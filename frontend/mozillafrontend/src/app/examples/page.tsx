'use client';

import React from 'react';
import Navbar from '/src/app/components/NavBar';

const ExamplesPage = () => {
    return (
      <div className="min-h-screen flex flex-col bg-gray-100">
        <Navbar />
        <div className="pt-20 p-4">
          <h1 className="text-3xl font-bold text-zinc-800">Examples</h1>
          <p className="mt-2 text-lg text-zinc-600">Here are some examples to help you get started.</p>
        </div>
      </div>
    );
  };
  
  export default ExamplesPage;
