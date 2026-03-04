import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SolveTrace — Decode Algorithms. Master Patterns.",
  description:
    "The ultimate companion for competitive programmers. Paste a problem URL and get instant step-by-step breakdowns, complexity analysis, and production-ready code.",
  keywords: [
    "competitive programming",
    "algorithm explainer",
    "LeetCode solutions",
    "Codeforces",
    "coding interview prep",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
