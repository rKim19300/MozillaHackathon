'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '/src/app/components/Navbar';
import axiosInstance from '../axiosInstance.js';

import io from "socket.io-client";

// Connect to the backend socket
const socket = io("http://localhost:5000");

const HomePage = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const [ summary, setSummary ] = useState("");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  
  const [url, setUrl] = useState<string>("");
  const [uploadStatus, setUploadStatus] = useState<string>("");

  const [ isFileMode, setIsFileMode ] = useState<boolean>(true);


  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  // Handle URL input change
  const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
    setUploadStatus(""); // Clear previous status when URL changes
  };

  // Handle file selection and generate a preview
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setSelectedFile(file);

      // Generate a preview for PDF or text files
      if (file.type === "application/pdf") {
        const fileURL = URL.createObjectURL(file);
        setFilePreview(fileURL); // Set URL for preview
      } else if (file.type === "text/plain") {
        const reader = new FileReader();
        reader.onload = () => {
          setFilePreview(reader.result as string); // Set text content for preview
        };
        reader.readAsText(file);
      } else {
        setFilePreview(null); // Clear preview for unsupported types
      }
    }
  };

  // Upload file and send to backend
  const sendData = async () => {
    if (!selectedFile) {
      alert("Please select a file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setSummary(""); // Reset summary

      // Send in file 
      let response;
      if (isFileMode) {
        response = await axiosInstance.post("/api/summarize/pdf", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
      }
      else {
        response = await axiosInstance.post("api/summarize/url", { url: url })
      }
      console.log("Uploaded successfully:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };  

  const sendPdf = async (pdf: FormData) => {

    // TODO convert the pdf into a byte stream

    setSummary("");
    await axiosInstance.post("/api/summarize/pdf", { pdf_stream: ""});
  }

  const sendUrl = async (url: string) => {

    // TODO convert the pdf into a byte stream

    setSummary("");
    await axiosInstance.post("/api/summarize/pdf", { url: url});
  }

  // The socket for constant updating
  useEffect(() => {
    socket.on('update-summary', (data) => {
      setSummary((prevSummary) => prevSummary + data.chunk.replace("</s>", " "))
    });

    return () => { socket.off('update-summary'); };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar />
      <div className="pt-20 min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center p-4 bg-white rounded-lg shadow-md">
          <h1 className="text-4xl font-bold text-zinc-500">Privacy Policies Simplified</h1>
          <p className="text-xl">Please upload a Privacy Policy pdf or txt file that you would like summarized.</p>
          { /* TODO Make a text box that takes in the UI along with its own separate button */ }
          { /* TODO Make form that holds the pdf */ }
          <input 
            type="file" 
            accept=".pdf,.txt" 
            onChange={handleFileChange}
            className="mt-4"
          />

          {/* URL input */}
          <input
            type="text"
            placeholder="Enter a URL"
            value={url}
            onChange={handleUrlChange}
            className="mt-4 p-2 border rounded-lg w-full"
          />

          {/* Preview area */}
          <div className="mt-4 border p-4 rounded-lg bg-gray-50">
            {filePreview ? (
              selectedFile?.type === "application/pdf" ? (
                <iframe
                  src={filePreview}
                  title="PDF Preview"
                  className="w-full h-96 border rounded-lg"
                ></iframe>
              ) : (
                <pre className="text-left whitespace-pre-wrap">
                  {filePreview}
                </pre>
              )
            ) : (
              <p>No preview available.</p>
            )}
          </div>
          <button 
            className="mt-4 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700" 
            onClick={() => sendData()}
            >
            Upload
          </button>
          { /* TODO Re-format summary, it has newlines in it, which don't render on the page */ }
          <p>{ summary }</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;