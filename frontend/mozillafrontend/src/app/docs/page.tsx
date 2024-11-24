'use client';

import React from 'react';
import Navbar from '../components/NavBar';

const DocsPage = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center p-24">
        <h1 className="text-3xl font-bold text-zinc-800">Documentation</h1>
        <p className="mt-2 text-lg text-zinc-600">Here you can find detailed documentation about the project.</p>
      </main>
    </div>
  );
};

export default DocsPage;