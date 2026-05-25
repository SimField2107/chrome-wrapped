"use client";

import { useEffect, useState } from "react";

const LOADING_MESSAGES = [
  "Loading your browsing history...",
  "Crunching the numbers...",
  "Finding your top sites...",
  "Analyzing your patterns...",
  "Computing your personality...",
  "Almost there...",
];

export function LoadingScreen() {
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="loading-screen">
      <div className="loading-content">
        <h1 className="loading-title">CHROME WRAPPED</h1>
        <div className="loading-spinner" />
        <p className="loading-message">{LOADING_MESSAGES[messageIndex]}</p>
      </div>
    </main>
  );
}
