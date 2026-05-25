import type { Metadata } from "next";
import { VT323, Press_Start_2P } from "next/font/google";
import "@/styles/globals.scss";

const vt323 = VT323({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-vt323",
});

const pressStart2P = Press_Start_2P({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-press-start",
});

export const metadata: Metadata = {
  title: "Chrome Wrapped",
  description: "Transform your browsing history into beautiful insights",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${vt323.variable} ${pressStart2P.variable}`}>
      <body>{children}</body>
    </html>
  );
}
