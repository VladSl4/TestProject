import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VibeLog — AI Log Analyzer",
  description: "Paste raw logs, get an AI-distilled summary.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
