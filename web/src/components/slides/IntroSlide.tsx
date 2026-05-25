"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

const BOOT_MESSAGES = [
  "> INITIALIZING CHROME_WRAPPED.EXE...",
  "> LOADING BROWSING HISTORY...",
  "> ANALYZING 365 DAYS OF DATA...",
  "> CATEGORIZING WEBSITES...",
  "> COMPUTING PERSONALITY PROFILE...",
  "> GENERATING INSIGHTS...",
  "> READY_",
];

export function IntroSlide() {
  const [visibleLines, setVisibleLines] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setVisibleLines((prev) => Math.min(prev + 1, BOOT_MESSAGES.length));
    }, 400);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="slide slide-intro">
      <motion.h1
        className="glitch-text"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        CHROME WRAPPED
      </motion.h1>

      <motion.p
        className="subtitle"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        Your year on the internet
      </motion.p>

      <div className="boot-log">
        {BOOT_MESSAGES.slice(0, visibleLines).map((msg, i) => (
          <motion.p
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.2 }}
          >
            {msg}
            {i === visibleLines - 1 && i === BOOT_MESSAGES.length - 1 && (
              <span className="cursor">█</span>
            )}
          </motion.p>
        ))}
      </div>
    </div>
  );
}
