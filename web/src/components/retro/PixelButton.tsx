"use client";

import { ButtonHTMLAttributes, ReactNode } from "react";

interface PixelButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary";
}

export function PixelButton({
  children,
  variant = "primary",
  className = "",
  ...props
}: PixelButtonProps) {
  return (
    <button className={`pixel-btn pixel-btn--${variant} ${className}`} {...props}>
      {children}
    </button>
  );
}
