"use client";

import { ReactNode } from "react";

interface Window98Props {
  title: string;
  children: ReactNode;
}

export function Window98({ title, children }: Window98Props) {
  return (
    <div className="window98">
      <div className="window98-titlebar">
        <span className="window98-title">{title}</span>
        <div className="window98-buttons">
          <button className="window98-btn minimize">_</button>
          <button className="window98-btn maximize">□</button>
          <button className="window98-btn close">×</button>
        </div>
      </div>
      <div className="window98-content">{children}</div>
    </div>
  );
}
