'use client';

import React from 'react';
import Navbar from '/src/app/components/Navbar';

const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar />
      <div className="pt-20 min-h-screen flex items-center justify-center bg-gray-100">
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