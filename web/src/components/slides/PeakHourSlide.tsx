"use client";

import { motion } from "framer-motion";
import type { HourlyVisits, TimeBadge } from "@chrome-wrapped/shared";
import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

interface PeakHourSlideProps {
  peakHour: number;
  timeBadge: TimeBadge;
  timeOfDay: HourlyVisits[];
}

const BADGE_LABELS: Record<TimeBadge, string> = {
  night_owl: "NIGHT OWL",
  early_bird: "EARLY BIRD",
  all_day_surfer: "ALL-DAY SURFER",
};

const BADGE_EMOJIS: Record<TimeBadge, string> = {
  night_owl: "🦉",
  early_bird: "🐦",
  all_day_surfer: "🏄",
};

export function PeakHourSlide({ peakHour, timeBadge, timeOfDay }: PeakHourSlideProps) {
  const formatHour = (hour: number) => {
    if (hour === 0) return "12AM";
    if (hour === 12) return "12PM";
    return hour > 12 ? `${hour - 12}PM` : `${hour}AM`;
  };

  const chartData = timeOfDay.map((h) => ({
    hour: formatHour(h.hour),
    visits: h.visits,
  }));

  return (
    <div className="slide slide-peak-hour">
      <motion.p
        className="label"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        Your peak browsing hour
      </motion.p>

      <motion.h2
        className="big-number"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
      >
        {formatHour(peakHour)}
      </motion.h2>

      <motion.div
        className="chart-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        <ResponsiveContainer width="100%" height={200}>
          <RadarChart data={chartData} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
            <PolarGrid stroke="#404060" />
            <PolarAngleAxis dataKey="hour" tick={{ fill: "#a0a0b0", fontSize: 10 }} />
            <Radar
              dataKey="visits"
              stroke="#c44cff"
              fill="#c44cff"
              fillOpacity={0.3}
            />
          </RadarChart>
        </ResponsiveContainer>
      </motion.div>

      <motion.p
        className="badge"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        {BADGE_EMOJIS[timeBadge]} {BADGE_LABELS[timeBadge]}
      </motion.p>
    </div>
  );
}
