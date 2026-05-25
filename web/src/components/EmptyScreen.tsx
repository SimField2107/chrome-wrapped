"use client";

import Link from "next/link";
import { PixelButton } from "@/components/retro/PixelButton";

export function EmptyScreen() {
  return (
    <main className="empty-screen">
      <div className="empty-content">
        <h1 className="empty-title">No Data Found</h1>
        <p className="empty-message">
          It looks like you don&apos;t have any browsing history to analyze.
          Browse the web for a while and come back to generate your Wrapped!
        </p>
        <div className="empty-tips">
          <h2>Tips:</h2>
          <ul>
            <li>Make sure you&apos;ve granted the extension access to your history</li>
            <li>Try selecting a longer time range in the extension settings</li>
            <li>Chrome history may be cleared or limited by your settings</li>
          </ul>
        </div>
        <Link href="/">
          <PixelButton>Go Home</PixelButton>
        </Link>
      </div>
    </main>
  );
}
