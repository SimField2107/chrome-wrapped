"use client";

import { useState, useCallback, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { Insights } from "@chrome-wrapped/shared";
import { Window98 } from "@/components/retro/Window98";
import { CRTScanlines } from "@/components/retro/CRTScanlines";
import {
  IntroSlide,
  TotalsSlide,
  TopSitesSlide,
  PeakHourSlide,
  SessionSlide,
  DayOfWeekSlide,
  CategoriesSlide,
  HeatmapSlide,
  PersonalitySlide,
  FinaleSlide,
} from "@/components/slides";

interface StoryPlayerProps {
  insights: Insights;
}

const SLIDE_TITLES = [
  "boot.exe",
  "stats.dat",
  "top_sites.html",
  "time.log",
  "sessions.bin",
  "week.csv",
  "categories.pie",
  "heatmap.bmp",
  "personality.exe",
  "finale.txt",
];

export function StoryPlayer({ insights }: StoryPlayerProps) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const totalSlides = SLIDE_TITLES.length;

  const goNext = useCallback(() => {
    setCurrentSlide((prev) => Math.min(prev + 1, totalSlides - 1));
  }, [totalSlides]);

  const goPrev = useCallback(() => {
    setCurrentSlide((prev) => Math.max(prev - 1, 0));
  }, []);

  const goToSlide = useCallback((index: number) => {
    setCurrentSlide(Math.max(0, Math.min(index, totalSlides - 1)));
  }, [totalSlides]);

  const handleReplay = useCallback(() => {
    setCurrentSlide(0);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === " ") {
        e.preventDefault();
        goNext();
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        goPrev();
      } else if (e.key === "p") {
        setIsPaused((prev) => !prev);
      } else if (e.key === "Home") {
        goToSlide(0);
      } else if (e.key === "End") {
        goToSlide(totalSlides - 1);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [goNext, goPrev, goToSlide, totalSlides]);

  useEffect(() => {
    const handleTouch = (() => {
      let startX = 0;
      let startY = 0;

      return {
        start: (e: TouchEvent) => {
          startX = e.touches[0].clientX;
          startY = e.touches[0].clientY;
        },
        end: (e: TouchEvent) => {
          const endX = e.changedTouches[0].clientX;
          const endY = e.changedTouches[0].clientY;
          const diffX = endX - startX;
          const diffY = endY - startY;

          if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
            if (diffX < 0) goNext();
            else goPrev();
          }
        },
      };
    })();

    window.addEventListener("touchstart", handleTouch.start);
    window.addEventListener("touchend", handleTouch.end);
    return () => {
      window.removeEventListener("touchstart", handleTouch.start);
      window.removeEventListener("touchend", handleTouch.end);
    };
  }, [goNext, goPrev]);

  const renderSlide = () => {
    switch (currentSlide) {
      case 0:
        return <IntroSlide />;
      case 1:
        return <TotalsSlide totals={insights.totals} />;
      case 2:
        return <TopSitesSlide sites={insights.topSites} />;
      case 3:
        return (
          <PeakHourSlide
            peakHour={insights.peakHour}
            timeBadge={insights.timeBadge}
            timeOfDay={insights.timeOfDay}
          />
        );
      case 4:
        return (
          <SessionSlide
            session={insights.session}
            domainDiscovery={insights.domainDiscovery}
          />
        );
      case 5:
        return (
          <DayOfWeekSlide
            dayOfWeek={insights.dayOfWeek}
            mostChronicallyOnlineDay={insights.mostChronicallyOnlineDay}
          />
        );
      case 6:
        return (
          <CategoriesSlide
            categories={insights.topCategories}
            guiltyPleasure={insights.guiltyPleasureCategory}
          />
        );
      case 7:
        return (
          <HeatmapSlide
            heatmap={insights.heatmap}
            streaks={insights.streaks}
          />
        );
      case 8:
        return <PersonalitySlide personality={insights.personality} />;
      case 9:
        return <FinaleSlide insights={insights} onReplay={handleReplay} />;
      default:
        return null;
    }
  };

  return (
    <div className="story-player">
      <CRTScanlines />

      <div className="progress-bar">
        {SLIDE_TITLES.map((_, i) => (
          <button
            key={i}
            className={`progress-segment ${i <= currentSlide ? "active" : ""} ${
              i === currentSlide ? "current" : ""
            }`}
            onClick={() => goToSlide(i)}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>

      <div
        className="slide-container"
        onClick={currentSlide < totalSlides - 1 ? goNext : undefined}
      >
        <Window98 title={SLIDE_TITLES[currentSlide]}>
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.3 }}
            >
              {renderSlide()}
            </motion.div>
          </AnimatePresence>
        </Window98>
      </div>

      <div className="nav-hint">
        <span>← →</span> or <span>swipe</span> to navigate |{" "}
        <span>{currentSlide + 1}/{totalSlides}</span>
      </div>
    </div>
  );
}
