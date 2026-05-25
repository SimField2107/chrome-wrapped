"use client";

import { motion } from "framer-motion";
import type { SessionInfo, DomainDiscovery } from "@chrome-wrapped/shared";

interface SessionSlideProps {
  session: SessionInfo;
  domainDiscovery: DomainDiscovery;
}

export function SessionSlide({ session, domainDiscovery }: SessionSlideProps) {
  const formatDuration = (minutes: number) => {
    if (minutes < 60) return `${minutes} minutes`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours} hours`;
  };

  return (
    <div className="slide slide-session">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Your Browsing Sessions
      </motion.h2>

      <motion.div
        className="session-stat"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        <p className="label">Longest session</p>
        <h3 className="session-value">{formatDuration(session.longestSessionMinutes)}</h3>
        <p className="session-detail">
          on {session.longestSessionDomain || "various sites"}
        </p>
      </motion.div>

      <motion.div
        className="discovery-stats"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="discovery-stat">
          <span className="discovery-value">{domainDiscovery.newDomains}</span>
          <span className="discovery-label">New discoveries</span>
          {domainDiscovery.topNewDomain && (
            <span className="discovery-top">Top: {domainDiscovery.topNewDomain}</span>
          )}
        </div>
        <div className="discovery-stat">
          <span className="discovery-value">{domainDiscovery.returningDomains}</span>
          <span className="discovery-label">Ride or dies</span>
          {domainDiscovery.topRideOrDie && (
            <span className="discovery-top">Fave: {domainDiscovery.topRideOrDie}</span>
          )}
        </div>
      </motion.div>
    </div>
  );
}
