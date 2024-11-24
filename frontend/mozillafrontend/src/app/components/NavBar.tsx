// components/Navbar.tsx
"use client";

import React, { useState } from "react";
import Link from "next/link";

const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="fixed top-0 left-0 w-full flex items-center justify-between flex-wrap bg-indigo-900 p-6 shadow-lg z-10">
      <div className="flex items-center flex-shrink-0 text-white mr-6">
        <span className="font-semibold text-xl tracking-tight">SafeScan</span>
      </div>

      {/* Mobile Menu Button */}
      <div className="block lg:hidden">
        <button
          className="flex items-center px-3 py-2 border rounded text-zinc-200 border-zinc-400 hover:text-white hover:border-white"
          onClick={toggleMobileMenu}
        >
          <svg
            className="fill-current h-3 w-3"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <title>Menu</title>
            <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
          </svg>
        </button>
      </div>

      {/* Menu Items (Desktop & Mobile) */}
      <div
        className={`w-full block flex-grow lg:flex lg:items-center lg:w-auto ${
          isMobileMenuOpen ? "block" : "hidden"
        }`}
      >
        <div className="text-sm lg:flex-grow">
          <Link
            href="/"
            className="block mt-4 lg:inline-block lg:mt-0 text-zinc-200 hover:text-white mr-4"
          >
            Home
          </Link>
          <Link
            href="/about"
            className="block mt-4 lg:inline-block lg:mt-0 text-zinc-200 hover:text-white mr-4"
          >
            About the Project
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
