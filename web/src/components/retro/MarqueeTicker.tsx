"use client";

interface MarqueeTickerProps {
  items: string[];
}

export function MarqueeTicker({ items }: MarqueeTickerProps) {
  const content = items.join(" | ");

  return (
    <div className="marquee-ticker">
      <div className="marquee-content">
        <span>{content}</span>
        <span>{content}</span>
      </div>
    </div>
  );
}
