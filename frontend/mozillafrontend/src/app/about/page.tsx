"use client";

import React from "react";
import Navbar from "../components/Navbar";

const DocsPage = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center p-24">
        <h1 className="text-3xl font-bold text-zinc-800">About the Project</h1>
        <br />
        <p className="mt-2 text-lg text-zinc-600">
          For this Hackathon, we were challenged to build an AI solution using
          Mozilla's Llamafile to protect users personal activities and
          information online.
        </p>
        <br />
        <p className="mt-2 text-lg text-zinc-600">
          Users are often overwhelmed by long, complex, and legalistic Terms of
          Service (ToS) and Privacy Policy agreements when interacting with
          online platforms. Despite being essential for user protection, these
          agreements are rarely read or understood by the average consumer. This
          leaves a user vulnerable to misuse of their data and privacy
          violations.
        </p>
        <br />
        <p className="mt-2 text-lg text-zinc-600">
          Our solution leverages Mozilla's Llamafile AI technology to empower
          users to make informed decisions about the services they use by
          simplifying the process of understanding complicated ToS and Privacy
          Policy agreements.
        </p>
        <br />
        <h3 className="text-2xl font-semibold text-zinc-800 mt-8 mb-4">
          Technology Stack
        </h3>
        <ul className="list-disc pl-6 mb-8">
          <li>
            <strong className="mt-2 text-lg text-zinc-600">Next.js</strong>{" "}
            (Frontend)
          </li>
          <li>
            <strong className="mt-2 text-lg text-zinc-600">Flask</strong>{" "}
            (Backend)
          </li>
          <li>
            <strong className="mt-2 text-lg text-zinc-600">
              Beautiful Soup
            </strong>{" "}
            (Web Scraping)
          </li>
          <li>
            <strong className="mt-2 text-lg text-zinc-600">
              Mozilla's Llamafile
            </strong>{" "}
            (AI Engine)
          </li>
        </ul>
      </main>
    </div>
  );
};

export default DocsPage;
