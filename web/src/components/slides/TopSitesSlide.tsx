"use client";

import { motion } from "framer-motion";
import type { TopSite } from "@chrome-wrapped/shared";

interface TopSitesSlideProps {
  sites: TopSite[];
}

export function TopSitesSlide({ sites }: TopSitesSlideProps) {
  const topFive = sites.slice(0, 5);
  const maxVisits = topFive[0]?.visits || 1;

  return (
    <div className="slide slide-top-sites">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Your Top Sites
      </motion.h2>

      <ol className="top-sites-list">
        {topFive.map((site, i) => (
          <motion.li
            key={site.domain}
            className="top-site"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + i * 0.15 }}
          >
            <span className="rank">#{i + 1}</span>
            <img
              src={site.favicon}
              alt=""
              className="favicon"
              width={24}
              height={24}
            />
            <div className="site-info">
              <span className="domain">{site.domain}</span>
              <div className="bar-container">
                <motion.div
                  className="bar-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${(site.visits / maxVisits) * 100}%` }}
                  transition={{ delay: 0.5 + i * 0.1, duration: 0.5 }}
                />
              </div>
            </div>
            <span className="visits">{site.visits.toLocaleString()}</span>
          </motion.li>
        ))}
      </ol>
    </div>
  );
}
