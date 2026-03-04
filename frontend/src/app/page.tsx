"use client";

import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import styles from "./page.module.css";

const GITHUB_URL = "https://github.com/rafaelcapeloo/SolveTrace";

export default function LandingPage() {
  return (
    <div className={styles.page}>
      <Navbar />

      {/* Hero */}
      <section className={styles.hero}>
        <div className="container">
          <div className={styles.heroGrid}>
            {/* Left: text */}
            <div className={styles.heroContent}>
              <div className={styles.badge}>Open Source · Free Forever</div>
              <h1 className={styles.heroTitle}>
                Understand algorithms,
                <br />
                <span className="text-accent">not just solve them.</span>
              </h1>
              <p className={styles.heroDesc}>
                Paste a competitive programming problem URL from Codeforces, LeetCode, AtCoder, or HackerRank —
                and get a step-by-step solution with complexity analysis, code in 10 languages, and interview tips.
                Powered by your choice of LLM.
              </p>
              <div className={styles.heroCtas}>
                <Link href="/solve" className="btn btn-primary btn-lg">
                  Try It Now →
                </Link>
                <a
                  href={GITHUB_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-ghost btn-lg"
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style={{ marginRight: "8px" }}>
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                  View on GitHub
                </a>
              </div>
            </div>

            {/* Right: terminal preview */}
            <div className={styles.heroPreview}>
              <div className={styles.previewWindow}>
                <div className={styles.previewDots}>
                  <span /><span /><span />
                </div>
                <div className={styles.previewContent}>
                  <div className={styles.previewLine}>
                    <span className={styles.previewAccent}>$ solvetrace</span> analyze
                  </div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewMuted}>Scraping problem from Codeforces...</span>
                  </div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewMuted}>Querying RAG knowledge base...</span>
                  </div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewMuted}>Generating analysis with LLM...</span>
                  </div>
                  <div className={styles.previewLine}>&nbsp;</div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewAccent}>✓</span> Step-by-step approach (5 steps)
                  </div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewAccent}>✓</span> Complexity: O(n log n) time, O(n) space
                  </div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewAccent}>✓</span> Code solution in Python
                  </div>
                  <div className={styles.previewLine}>
                    <span className={styles.previewAccent}>✓</span> 3 key insights + interview tips
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className={styles.features}>
        <div className="container">
          <h2 className={styles.sectionTitle}>How It Works</h2>
          <div className={styles.featureGrid}>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z" fill="currentColor" /></svg>
              </div>
              <h3>Paste a URL</h3>
              <p>Support for Codeforces, LeetCode, AtCoder, and HackerRank. Auto-scrapes the problem statement, examples, and constraints.</p>
            </div>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z" fill="currentColor" /></svg>
              </div>
              <h3>AI Analysis</h3>
              <p>Get a step-by-step approach, complexity analysis with reasoning, key insights, common pitfalls, and interview tips.</p>
            </div>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z" fill="currentColor" /></svg>
              </div>
              <h3>Code Solutions</h3>
              <p>Clean, well-commented code in Python, C++, Java, JavaScript, Go, Rust, and 4 more languages with syntax highlighting.</p>
            </div>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor" /></svg>
              </div>
              <h3>Choose Your LLM</h3>
              <p>Run locally with Ollama (Qwen, LLaMA), or use cloud APIs — OpenAI GPT-4o, Google Gemini. Your keys, your choice.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className={styles.techStack}>
        <div className="container">
          <h2 className={styles.sectionTitle}>Built With</h2>
          <div className={styles.techGrid}>
            {[
              { name: "Next.js", desc: "React framework" },
              { name: "FastAPI", desc: "Python backend" },
              { name: "SQLite", desc: "Cache & persistence" },
              { name: "Ollama", desc: "Local LLM" },
              { name: "OpenAI", desc: "GPT models" },
              { name: "Gemini", desc: "Google AI" },
            ].map((tech) => (
              <div key={tech.name} className={styles.techBadge}>
                <span className={styles.techName}>{tech.name}</span>
                <span className={styles.techDesc}>{tech.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className={styles.cta}>
        <div className="container">
          <h2>Ready to solve smarter?</h2>
          <p>No signup, no limits, no cost. Just paste and learn.</p>
          <Link href="/solve" className="btn btn-primary btn-lg">
            Start Analyzing →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className="container">
          <p>
            <span className="text-accent">SolveTrace</span> — Open-source competitive programming analyzer.
            Built by{" "}
            <a href="https://github.com/rafaelcapeloo" target="_blank" rel="noopener noreferrer" className="text-accent">
              @rafaelcapeloo
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}
