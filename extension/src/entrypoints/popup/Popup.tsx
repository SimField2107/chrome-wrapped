import React, { useState } from "react";
import { fetchHistory } from "../../lib/history";
import { createRun } from "../../lib/api";

type Status = "idle" | "loading" | "success" | "error";

export function Popup() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<string>("");

  const handleGenerate = async () => {
    setStatus("loading");
    setError(null);
    setProgress("Fetching your browsing history...");

    try {
      const history = await fetchHistory();
      setProgress(`Found ${history.length} pages. Analyzing...`);

      const now = new Date();
      const yearAgo = new Date(now);
      yearAgo.setFullYear(yearAgo.getFullYear() - 1);

      const { runId } = await createRun({
        history,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        rangeStart: yearAgo.toISOString(),
        rangeEnd: now.toISOString(),
      });

      setProgress("Opening your Wrapped...");
      setStatus("success");

      chrome.tabs.create({
        url: `http://localhost:3001/wrapped/${runId}`,
      });
    } catch (err) {
      setStatus("error");
      let errorMessage = "Something went wrong";
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === "string") {
        errorMessage = err;
      } else {
        errorMessage = String(err);
      }
      console.error("Chrome Wrapped error:", err);
      setError(errorMessage);
    }
  };

  return (
    <div className="popup">
      <header className="header">
        <h1 className="title">Chrome Wrapped</h1>
        <p className="subtitle">Your year on the internet</p>
      </header>

      <main className="content">
        {status === "idle" && (
          <>
            <p className="description">
              Transform your browsing history into beautiful insights.
              See your most visited sites, peak hours, and browsing personality.
            </p>
            <button className="generate-btn" onClick={handleGenerate}>
              Generate My Wrapped
            </button>
            <p className="privacy-note">
              Your data is processed securely and deleted after 24 hours.
            </p>
          </>
        )}

        {status === "loading" && (
          <div className="loading">
            <div className="spinner" />
            <p className="progress">{progress}</p>
          </div>
        )}

        {status === "success" && (
          <div className="success">
            <p>Opening your Wrapped in a new tab...</p>
          </div>
        )}

        {status === "error" && (
          <div className="error">
            <p className="error-title">Oops!</p>
            <p className="error-message">{error}</p>
            <button className="retry-btn" onClick={handleGenerate}>
              Try Again
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
