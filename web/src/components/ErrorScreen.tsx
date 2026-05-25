"use client";

import Link from "next/link";
import { PixelButton } from "@/components/retro/PixelButton";

interface ErrorScreenProps {
  runId?: string;
}

export function ErrorScreen({ runId }: ErrorScreenProps) {
  const handleRetry = () => {
    window.location.reload();
  };

  return (
    <main className="error-screen">
      <div className="error-content">
        <h1 className="error-title">404.exe</h1>
        <p className="error-subtitle">Wrapped not found</p>
        <p className="error-message">
          We couldn&apos;t find your Chrome Wrapped. The link may have expired
          or the data is still being processed.
        </p>
        {runId && (
          <p className="error-run-id">
            Run ID: <code>{runId}</code>
          </p>
        )}
        <div className="error-actions">
          <PixelButton onClick={handleRetry}>Try Again</PixelButton>
          <Link href="/">
            <PixelButton variant="secondary">Go Home</PixelButton>
          </Link>
        </div>
      </div>
    </main>
  );
}
