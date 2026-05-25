"use client";

import { motion } from "framer-motion";
import type { InsightsTotals } from "@chrome-wrapped/shared";

interface TotalsSlideProps {
  totals: InsightsTotals;
}

export function TotalsSlide({ totals }: TotalsSlideProps) {
  return (
    <div className="slide slide-totals">
      <motion.p
        className="label"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        This year, you browsed
      </motion.p>

      <motion.h2
        className="big-number"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
      >
        {totals.pageviews.toLocaleString()}
      </motion.h2>

      <motion.p
        className="label"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        pages
      </motion.p>

      <motion.div
        className="sub-stats"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <div className="stat">
          <span className="stat-value">{totals.uniqueDomains.toLocaleString()}</span>
          <span className="stat-label">unique sites</span>
        </div>
        <div className="stat">
          <span className="stat-value">{totals.activeDays}</span>
          <span className="stat-label">active days</span>
        </div>
      </motion.div>
    </div>
  );
}
