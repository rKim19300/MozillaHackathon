'use client'

import React, { useState } from 'react';

const HomePage = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* Navigation Bar */}
      <nav className="flex items-center justify-between flex-wrap bg-zinc-900 p-6">
        <div className="flex items-center flex-shrink-0 text-white mr-6">
          <span className="font-semibold text-xl tracking-tight">Mozilla Hackathon</span>
        </div>
        
        {/* Mobile Menu Button */}
        <div className="block lg:hidden">
          <button
            className="flex items-center px-3 py-2 border rounded text-zinc-200 border-zinc-400 hover:text-white hover:border-white"
            onClick={toggleMobileMenu}
          >
            <svg className="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <title>Menu</title>
              <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/>
            </svg>
          </button>
        </div>

        {/* Menu Items (Desktop & Mobile) */}
        <div className={`w-full block flex-grow lg:flex lg:items-center lg:w-auto ${isMobileMenuOpen ? "block" : "hidden"}`}>
          <div className="text-sm lg:flex-grow">
            <a href="#responsive-header" className="block mt-4 lg:inline-block lg:mt-0 text-zinc-200 hover:text-white mr-4">
              Docs
            </a>
            <a href="#responsive-header" className="block mt-4 lg:inline-block lg:mt-0 text-zinc-200 hover:text-white mr-4">
              Examples
            </a>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center p-4 bg-white rounded-lg shadow-md">
          <h1 className="text-4xl font-bold text-zinc-500">Privacy Policies Simplified</h1>
          <p className="text-xl">Please upload a Privacy Policy pdf or txt file that you would like summarized.</p>
          <button className="mt-4 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
            Upload
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
