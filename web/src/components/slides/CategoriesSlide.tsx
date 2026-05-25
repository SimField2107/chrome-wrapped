"use client";

import { motion } from "framer-motion";
import type { TopCategory } from "@chrome-wrapped/shared";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";

interface CategoriesSlideProps {
  categories: TopCategory[];
  guiltyPleasure: string;
}

const COLORS = [
  "#ff6b9d",
  "#c44cff",
  "#6b9dff",
  "#9dff6b",
  "#ffb86b",
  "#6bffff",
  "#ff6b6b",
  "#b86bff",
];

const CATEGORY_LABELS: Record<string, string> = {
  social: "Social Media",
  entertainment: "Entertainment",
  news: "News",
  shopping: "Shopping",
  development: "Dev & Tech",
  learning: "Learning",
  work: "Work",
  communication: "Communication",
  finance: "Finance",
  health: "Health",
  gaming: "Gaming",
  search: "Search",
  other: "Other",
};

export function CategoriesSlide({ categories, guiltyPleasure }: CategoriesSlideProps) {
  const topFive = categories.slice(0, 5);
  const chartData = topFive.map((cat) => ({
    name: CATEGORY_LABELS[cat.category] || cat.category,
    value: cat.visits,
  }));

  return (
    <div className="slide slide-categories">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        How You Spent Your Time
      </motion.h2>

      <motion.div
        className="chart-container"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={80}
              paddingAngle={2}
              dataKey="value"
              animationDuration={800}
            >
              {chartData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </motion.div>

      <div className="category-list">
        {topFive.map((cat, i) => (
          <motion.div
            key={cat.category}
            className="category-row"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 + i * 0.1 }}
          >
            <span
              className="category-dot"
              style={{ backgroundColor: COLORS[i % COLORS.length] }}
            />
            <span className="category-name">
              {CATEGORY_LABELS[cat.category] || cat.category}
            </span>
            <span className="category-pct">{cat.percentage.toFixed(0)}%</span>
          </motion.div>
        ))}
      </div>

      {guiltyPleasure && guiltyPleasure !== "other" && (
        <motion.div
          className="guilty-pleasure"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <p className="guilty-label">Your guilty pleasure:</p>
          <p className="guilty-category">
            {CATEGORY_LABELS[guiltyPleasure] || guiltyPleasure}
          </p>
          <p className="guilty-note">Your fastest growing category</p>
        </motion.div>
      )}
    </div>
  );
}
