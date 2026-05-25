"use client";

import { motion } from "framer-motion";
import { useCallback, useRef, useState } from "react";
import { toPng } from "html-to-image";
import type { Insights } from "@chrome-wrapped/shared";
import { PixelButton } from "@/components/retro/PixelButton";

interface FinaleSlideProps {
  insights: Insights;
  onReplay: () => void;
}

export function FinaleSlide({ insights, onReplay }: FinaleSlideProps) {
  const shareCardRef = useRef<HTMLDivElement>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleShare = useCallback(async () => {
    if (!shareCardRef.current) return;

    setIsGenerating(true);
    try {
      const dataUrl = await toPng(shareCardRef.current, {
        width: 1080,
        height: 1920,
        pixelRatio: 1,
      });

      const link = document.createElement("a");
      link.download = "chrome-wrapped-2024.png";
      link.href = dataUrl;
      link.click();
    } catch (error) {
      console.error("Failed to generate share card:", error);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const CLUB_NAMES: Record<string, string> = {
    rabbit_hole_researcher: "RABBIT HOLE RESEARCHER",
    doomscroller: "DOOMSCROLLER",
    hustle_tab_hoarder: "HUSTLE TAB-HOARDER",
    comfort_rewatcher: "COMFORT RE-WATCHER",
    niche_forum_lurker: "NICHE FORUM LURKER",
    casual_surfer: "CASUAL SURFER",
  };

  return (
    <div className="slide slide-finale">
      <motion.h2
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
      >
        That&apos;s a wrap!
      </motion.h2>

      <motion.p
        className="label"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        Thanks for browsing with Chrome
      </motion.p>

      <motion.div
        className="actions"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <PixelButton onClick={handleShare} disabled={isGenerating}>
          {isGenerating ? "Generating..." : "Download Share Card"}
        </PixelButton>
        <PixelButton variant="secondary" onClick={onReplay}>
          Replay
        </PixelButton>
      </motion.div>

      <div
        ref={shareCardRef}
        className="share-card"
        style={{ position: "absolute", left: "-9999px", top: "-9999px" }}
      >
        <div className="share-card-content">
          <h1>CHROME WRAPPED 2024</h1>
          <div className="share-stats">
            <p className="share-stat">
              <span>{insights.totals.pageviews.toLocaleString()}</span> pages browsed
            </p>
            <p className="share-stat">
              <span>{insights.totals.uniqueDomains}</span> unique sites
            </p>
            <p className="share-stat">
              Top site: <span>{insights.topSites[0]?.domain || "N/A"}</span>
            </p>
          </div>
          <div className="share-personality">
            <p>I am a</p>
            <h2>{CLUB_NAMES[insights.personality.club] || insights.personality.club}</h2>
          </div>
          <p className="share-url">chrome-wrapped.app</p>
        </div>
      </div>
    </div>
  );
}
