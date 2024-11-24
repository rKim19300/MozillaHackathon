'use client';

import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
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

  const [isFileMode, setIsFileMode] = useState<boolean>(true); // Toggle between File and URL modes


  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

   // Toggle between file and URL submission modes
   const toggleMode = () => {
    // Release the Blob URL before switching modes
    if (filePreview) {
      URL.revokeObjectURL(filePreview); // Cleanup Blob URL when switching modes
    }
    
    // Reset states and switch mode
    setIsFileMode((prevMode) => !prevMode);
    setUploadStatus(""); // Reset upload status when switching modes
    setSelectedFile(null); // Clear file selection
    setUrl(""); // Clear URL input
    setFilePreview(null); // Clear file preview
  };

  
  // Handle URL input change
  const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value || "");
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
    } else {
      setSelectedFile(null); // Ensure controlled state when no file is selected
    }
  };

  // Upload file and send to backend
  const sendPdf = async () => {
    if (!selectedFile) {
      alert("Please select a file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setSummary(""); // Reset summary

      // Send in file 
      const response = await axiosInstance.post("/api/summarize/pdf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    
      console.log("Uploaded successfully:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };  

  const sendUrl = async () => {

    if (!url) {
      alert("Please enter a url before upload.");
      return;
    }

    try {
      setSummary(""); // Reset summary

      // Send in file 
      const response = await axiosInstance.post("/api/summarize/url", { url: url});
    
      console.log("Uploaded successfully:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  }

  // The socket for constant updating
  useEffect(() => {
    socket.on('update-summary', (data) => {
      setSummary((prevSummary) => prevSummary + data.chunk.replace("</s>", " "));
    });

    return () => { socket.off('update-summary'); };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar />
      <div className="pt-20 min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center p-4 bg-white rounded-lg shadow-md">
          <h1 className="text-4xl font-bold text-indigo-500">Privacy Policies Simplified</h1>
          <p className="text-m">Please upload a Privacy Policy pdf or txt file that you would like summarized.</p>
          {/* Toggle Mode Button */}
          <button 
            className="mt-4 p-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-300"
            onClick={toggleMode}
          >
            Switch to {isFileMode ? "URL Submission" : "File Upload"}
          </button>

          {isFileMode ? (
            // File Upload Mode
            <div className="mt-4">
              <input 
                type="file" 
                accept=".pdf,.txt" 
                onChange={handleFileChange}
                className="mt-4"
              />
              {filePreview && (
                <div className="mt-4 border p-4 rounded-lg bg-gray-50">
                  {selectedFile?.type === "application/pdf" ? (
                    <iframe
                      src={filePreview}
                      title="PDF Preview"
                      className="w-full h-96 border rounded-lg"
                    ></iframe>
                  ) : (
                    <pre className="text-left whitespace-pre-wrap">{filePreview}</pre>
                  )}
                </div>
              )}
            </div>
          ) : (
            // URL Submission Mode
            <div className="mt-4">
              <input
                type="text"
                placeholder="Enter a URL"
                value={url}
                onChange={handleUrlChange}
                className="mt-4 p-2 border rounded-lg w-full"
              />
            </div>
          )}
          { /* TODO Make a text box that takes in the UI along with its own separate button */ }
          { /* TODO Make form that holds the pdf */ }
          <button 
            className="mt-4 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700" 
            onClick={() => (isFileMode) ? sendPdf() : sendUrl()}
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