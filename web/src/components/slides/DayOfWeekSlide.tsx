"use client";

import { motion } from "framer-motion";
import type { DayOfWeekVisits } from "@chrome-wrapped/shared";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

interface DayOfWeekSlideProps {
  dayOfWeek: DayOfWeekVisits[];
  mostChronicallyOnlineDay: {
    date: string;
    visits: number;
    topDomain: string;
  };
}

const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export function DayOfWeekSlide({
  dayOfWeek,
  mostChronicallyOnlineDay,
}: DayOfWeekSlideProps) {
  const chartData = dayOfWeek.map((d) => ({
    day: DAY_NAMES[d.dayOfWeek],
    visits: d.visits,
  }));

  const busiestDay = dayOfWeek.reduce(
    (max, d) => (d.visits > max.visits ? d : max),
    dayOfWeek[0]
  );

  const formatDate = (dateStr: string) => {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };

  return (
    <div className="slide slide-day-of-week">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Your Week in Browsing
      </motion.h2>

      <motion.div
        className="chart-container"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={chartData} margin={{ top: 10, right: 10, bottom: 20, left: 10 }}>
            <XAxis
              dataKey="day"
              tick={{ fill: "#a0a0b0", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis hide />
            <Bar
              dataKey="visits"
              fill="#6b9dff"
              radius={[4, 4, 0, 0]}
              animationDuration={800}
            />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      <motion.p
        className="busiest-day"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        {DAY_NAMES[busiestDay?.dayOfWeek || 0]} is your most active day
      </motion.p>

      {mostChronicallyOnlineDay.visits > 0 && (
        <motion.div
          className="online-day"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <p className="online-label">Most chronically online day:</p>
          <p className="online-date">{formatDate(mostChronicallyOnlineDay.date)}</p>
          <p className="online-visits">
            {mostChronicallyOnlineDay.visits} pages on {mostChronicallyOnlineDay.topDomain}
          </p>
        </motion.div>
      )}
    </div>
  );
}
