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

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  // Query the terms of service
  const sendTerms = async () => {
    setSummary("");
    // TODO replace the terms with a file
    await axiosInstance.post("/api/summarize", { terms: "terms"});
  };

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
          <button 
            className="mt-4 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700" 
            onClick={() => sendTerms()}
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