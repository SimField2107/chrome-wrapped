"use client";

import { motion } from "framer-motion";
import type { HeatmapDay, Streaks } from "@chrome-wrapped/shared";
import { useMemo } from "react";

interface HeatmapSlideProps {
  heatmap: HeatmapDay[];
  streaks: Streaks;
}

export function HeatmapSlide({ heatmap, streaks }: HeatmapSlideProps) {
  const { grid, maxVisits, months } = useMemo(() => {
    if (heatmap.length === 0) {
      return { grid: [], maxVisits: 0, months: [] };
    }

    const visitMap = new Map(heatmap.map((d) => [d.date, d.visits]));
    const maxV = Math.max(...heatmap.map((d) => d.visits), 1);

    const startDate = new Date(heatmap[0].date);
    const endDate = new Date(heatmap[heatmap.length - 1].date);

    const weeks: { date: string; visits: number }[][] = [];
    const monthLabels: { label: string; weekIndex: number }[] = [];
    let currentWeek: { date: string; visits: number }[] = [];
    let lastMonth = -1;

    const current = new Date(startDate);
    current.setDate(current.getDate() - current.getDay());

    while (current <= endDate || currentWeek.length > 0) {
      const dateStr = current.toISOString().split("T")[0];
      const visits = visitMap.get(dateStr) || 0;

      if (current.getMonth() !== lastMonth) {
        monthLabels.push({
          label: current.toLocaleDateString("en-US", { month: "short" }),
          weekIndex: weeks.length,
        });
        lastMonth = current.getMonth();
      }

      currentWeek.push({ date: dateStr, visits });

      if (current.getDay() === 6) {
        weeks.push(currentWeek);
        currentWeek = [];
      }

      current.setDate(current.getDate() + 1);
      if (current > endDate && currentWeek.length === 0) break;
    }

    if (currentWeek.length > 0) {
      weeks.push(currentWeek);
    }

    return { grid: weeks, maxVisits: maxV, months: monthLabels };
  }, [heatmap]);

  const getColor = (visits: number) => {
    if (visits === 0) return "#1a1a2e";
    const intensity = Math.min(visits / maxVisits, 1);
    if (intensity < 0.25) return "#3d2a4d";
    if (intensity < 0.5) return "#6b3d7a";
    if (intensity < 0.75) return "#9d4caa";
    return "#c44cff";
  };

  return (
    <div className="slide slide-heatmap">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Your Browsing Heatmap
      </motion.h2>

      <motion.div
        className="heatmap-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div className="heatmap-months">
          {months.slice(0, 12).map((m, i) => (
            <span
              key={i}
              className="heatmap-month"
              style={{ gridColumnStart: m.weekIndex + 1 }}
            >
              {m.label}
            </span>
          ))}
        </div>
        <div className="heatmap-grid">
          {grid.slice(0, 53).map((week, wi) => (
            <div key={wi} className="heatmap-week">
              {week.map((day, di) => (
                <motion.div
                  key={di}
                  className="heatmap-day"
                  style={{ backgroundColor: getColor(day.visits) }}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3 + wi * 0.01 + di * 0.01 }}
                  title={`${day.date}: ${day.visits} visits`}
                />
              ))}
            </div>
          ))}
        </div>
      </motion.div>

      <motion.div
        className="streaks"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <div className="streak">
          <span className="streak-value">{streaks.longestOnStreak}</span>
          <span className="streak-label">day streak</span>
        </div>
        <div className="streak">
          <span className="streak-value">{streaks.longestOffStreak}</span>
          <span className="streak-label">days offline</span>
        </div>
      </motion.div>
    </div>
  );
}
