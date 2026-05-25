"use client";

import { motion } from "framer-motion";
import type { Personality } from "@chrome-wrapped/shared";

interface PersonalitySlideProps {
  personality: Personality;
}

const CLUB_NAMES: Record<string, string> = {
  rabbit_hole_researcher: "THE RABBIT HOLE RESEARCHER",
  doomscroller: "THE DOOMSCROLLER",
  hustle_tab_hoarder: "THE HUSTLE TAB-HOARDER",
  comfort_rewatcher: "THE COMFORT RE-WATCHER",
  niche_forum_lurker: "THE NICHE FORUM LURKER",
  casual_surfer: "THE CASUAL SURFER",
};

const ROLE_NAMES: Record<string, string> = {
  archivist: "ARCHIVIST",
  explorer: "EXPLORER",
  loyalist: "LOYALIST",
  multitasker: "MULTITASKER",
  lurker: "LURKER",
};

const CLUB_EMOJIS: Record<string, string> = {
  rabbit_hole_researcher: "🐰🕳️",
  doomscroller: "📱💀",
  hustle_tab_hoarder: "💼📑",
  comfort_rewatcher: "🛋️🔁",
  niche_forum_lurker: "👀💬",
  casual_surfer: "🏄🌊",
};

export function PersonalitySlide({ personality }: PersonalitySlideProps) {
  return (
    <div className="slide slide-personality">
      <motion.p
        className="label"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        You are...
      </motion.p>

      <motion.div
        className="club-emoji"
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
      >
        {CLUB_EMOJIS[personality.club] || "🌐"}
      </motion.div>

      <motion.h2
        className="club-name"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        {CLUB_NAMES[personality.club] || personality.club.replace(/_/g, " ").toUpperCase()}
      </motion.h2>

      <motion.p
        className="role"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        Role: {ROLE_NAMES[personality.role] || personality.role.toUpperCase()}
      </motion.p>

      <motion.p
        className="blurb"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        {personality.blurb}
      </motion.p>
    </div>
  );
}
