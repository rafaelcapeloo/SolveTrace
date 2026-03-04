"use client";

import { useState, useEffect, useRef, useCallback, Suspense } from "react";
import Navbar from "@/components/layout/Navbar";
import { analyzeRequest, getConfig } from "@/services/api";
import type { AnalysisResult } from "@/types";
import type { LLMProvider } from "@/services/api";
import styles from "./page.module.css";
import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
import cpp from "highlight.js/lib/languages/cpp";
import java from "highlight.js/lib/languages/java";
import javascript from "highlight.js/lib/languages/javascript";
import typescript from "highlight.js/lib/languages/typescript";
import go from "highlight.js/lib/languages/go";
import rust from "highlight.js/lib/languages/rust";
import csharp from "highlight.js/lib/languages/csharp";
import kotlin from "highlight.js/lib/languages/kotlin";
import swift from "highlight.js/lib/languages/swift";

// Register languages
hljs.registerLanguage("python", python);
hljs.registerLanguage("cpp", cpp);
hljs.registerLanguage("java", java);
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("typescript", typescript);
hljs.registerLanguage("go", go);
hljs.registerLanguage("rust", rust);
hljs.registerLanguage("csharp", csharp);
hljs.registerLanguage("kotlin", kotlin);
hljs.registerLanguage("swift", swift);

const LANGUAGES = [
    { value: "python", label: "Python" },
    { value: "cpp", label: "C++" },
    { value: "java", label: "Java" },
    { value: "javascript", label: "JavaScript" },
    { value: "typescript", label: "TypeScript" },
    { value: "go", label: "Go" },
    { value: "rust", label: "Rust" },
    { value: "csharp", label: "C#" },
    { value: "kotlin", label: "Kotlin" },
    { value: "swift", label: "Swift" },
];

/* Syntax-highlighted code block */
function HighlightedCode({ code, language }: { code: string; language: string }) {
    const codeRef = useRef<HTMLElement>(null);

    useEffect(() => {
        if (codeRef.current) {
            codeRef.current.removeAttribute("data-highlighted");

            // Clean up markdown ticks if the LLM included them inside the JSON string
            let cleanCode = code;
            if (cleanCode.startsWith("```")) {
                cleanCode = cleanCode.replace(/^```[a-zA-Z\+#]*\n?/, "").replace(/\n?```\s*$/, "");
            }

            codeRef.current.textContent = cleanCode;
            hljs.highlightElement(codeRef.current);
        }
    }, [code, language]);

    const langMap: Record<string, string> = {
        "c++": "cpp", "c#": "csharp", "js": "javascript", "ts": "typescript",
    };
    const hljsLang = langMap[language.toLowerCase()] || language.toLowerCase();

    return (
        <pre className={styles.codeBlockBody}>
            <code ref={codeRef} className={`language-${hljsLang}`}>
                {code}
            </code>
        </pre>
    );
}

function SolveContent() {
    const [mode, setMode] = useState<"url" | "paste">("url");
    const [url, setUrl] = useState("");
    const [problemText, setProblemText] = useState("");
    const [language, setLanguage] = useState("python");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [activeCodeLang, setActiveCodeLang] = useState("");
    const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());

    // LLM provider state
    const [providers, setProviders] = useState<LLMProvider[]>([]);
    const [selectedProvider, setSelectedProvider] = useState("");
    const [selectedModel, setSelectedModel] = useState("");

    // Fetch available LLM providers on mount
    useEffect(() => {
        getConfig()
            .then((config) => {
                setProviders(config.providers);
                setSelectedProvider(config.current_provider);
                const curr = config.providers.find(p => p.id === config.current_provider);
                if (curr && curr.models.length > 0) {
                    setSelectedModel(curr.models[0]);
                }
            })
            .catch(() => {
                // Backend not available yet — use default
                setProviders([]);
            });
    }, []);

    // Update model when provider changes
    useEffect(() => {
        if (!selectedProvider) return;
        const p = providers.find(prov => prov.id === selectedProvider);
        if (p && p.models.length > 0 && !p.models.includes(selectedModel)) {
            setSelectedModel(p.models[0]);
        }
    }, [selectedProvider, providers, selectedModel]);

    const handleAnalyze = async () => {
        setError("");
        setLoading(true);
        setResult(null);
        try {
            const data = await analyzeRequest(
                mode === "url" ? url : null,
                mode === "paste" ? problemText : null,
                language,
                selectedProvider || undefined,
                selectedModel || undefined,
            );
            setResult(data);
            setActiveCodeLang(language);
            if (data.approach) {
                setExpandedSteps(new Set(data.approach.map((_: unknown, i: number) => i)));
            }
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Analysis failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const toggleStep = useCallback((i: number) => {
        setExpandedSteps((prev) => {
            const next = new Set(prev);
            if (next.has(i)) next.delete(i);
            else next.add(i);
            return next;
        });
    }, []);

    return (
        <div className={styles.page}>
            <Navbar />
            <main className={styles.main}>
                <div className="container">
                    {/* Input */}
                    <section className={styles.inputSection}>
                        <h1>Analyze a Problem</h1>
                        <p className={styles.subtitle}>
                            Paste a competitive programming problem URL or text to get a step-by-step solution with complexity analysis, code, and interview tips.
                        </p>

                        <div className={styles.modeToggle}>
                            <button
                                className={`${styles.modeBtn} ${mode === "url" ? styles.modeBtnActive : ""}`}
                                onClick={() => setMode("url")}
                            >
                                Paste URL
                            </button>
                            <button
                                className={`${styles.modeBtn} ${mode === "paste" ? styles.modeBtnActive : ""}`}
                                onClick={() => setMode("paste")}
                            >
                                Paste Problem
                            </button>
                        </div>

                        {mode === "url" ? (
                            <div className={styles.inputGroup}>
                                <input
                                    type="url"
                                    placeholder="https://codeforces.com/problemset/problem/..."
                                    value={url}
                                    onChange={(e) => setUrl(e.target.value)}
                                />
                            </div>
                        ) : (
                            <div className={styles.inputGroup}>
                                <textarea
                                    rows={6}
                                    placeholder="Paste the full problem statement here..."
                                    value={problemText}
                                    onChange={(e) => setProblemText(e.target.value)}
                                />
                            </div>
                        )}

                        <div className={styles.inputGroup}>
                            <div className={styles.configRow}>
                                {/* Language selector */}
                                <div className={styles.langWrap}>
                                    <label className={styles.langLabel}>Solution Language</label>
                                    <select
                                        value={language}
                                        onChange={(e) => setLanguage(e.target.value)}
                                        className={styles.langSelect}
                                    >
                                        {LANGUAGES.map((l) => (
                                            <option key={l.value} value={l.value}>{l.label}</option>
                                        ))}
                                    </select>
                                </div>

                                {/* LLM Provider selector */}
                                {providers.length > 0 && (
                                    <>
                                        <div className={styles.langWrap}>
                                            <label className={styles.langLabel}>LLM Provider</label>
                                            <select
                                                value={selectedProvider}
                                                onChange={(e) => setSelectedProvider(e.target.value)}
                                                className={`${styles.langSelect} ${providers.find(p => p.id === selectedProvider && !p.available) ? styles.langSelectWarn : ""}`}
                                            >
                                                {providers.map((p) => (
                                                    <option key={p.id} value={p.id}>
                                                        {p.name}{!p.available ? " ⚠" : " ✓"}
                                                    </option>
                                                ))}
                                            </select>
                                            {(() => {
                                                const selected = providers.find(p => p.id === selectedProvider);
                                                if (selected && !selected.available) {
                                                    const envVar = selectedProvider === "gemini" ? "GEMINI_API_KEY" : selectedProvider === "openai" ? "OPENAI_API_KEY" : "OLLAMA_BASE_URL";
                                                    return (
                                                        <span className={styles.providerHint}>
                                                            ⚠ Set <code>{envVar}</code> in <code>.env</code>
                                                        </span>
                                                    );
                                                }
                                                if (selected && selected.available) {
                                                    return (
                                                        <span className={styles.providerHintOk}>
                                                            ✓ Configured
                                                        </span>
                                                    );
                                                }
                                                return null;
                                            })()}
                                        </div>

                                        {(() => {
                                            const p = providers.find(prov => prov.id === selectedProvider);
                                            if (p && p.models && p.models.length > 0) {
                                                return (
                                                    <div className={styles.langWrap}>
                                                        <label className={styles.langLabel}>Model</label>
                                                        <select
                                                            value={selectedModel}
                                                            onChange={(e) => setSelectedModel(e.target.value)}
                                                            className={styles.langSelect}
                                                        >
                                                            {p.models.map(m => (
                                                                <option key={m} value={m}>{m}</option>
                                                            ))}
                                                        </select>
                                                    </div>
                                                );
                                            }
                                            return null;
                                        })()}
                                    </>
                                )}
                            </div>

                            <button
                                className={`btn btn-primary btn-lg ${styles.analyzeBtn}`}
                                onClick={handleAnalyze}
                                disabled={loading || (mode === "url" ? !url : !problemText)}
                            >
                                {loading ? "Analyzing..." : "Analyze →"}
                            </button>
                        </div>
                    </section>

                    {/* Supported Platforms */}
                    {!result && !loading && (
                        <section className={styles.platforms}>
                            <h3>Supported Platforms</h3>
                            <div className={styles.platformList}>
                                {["Codeforces", "LeetCode", "AtCoder", "HackerRank"].map((p) => (
                                    <span key={p} className={styles.platformBadge}>{p}</span>
                                ))}
                            </div>
                        </section>
                    )}

                    {/* Error */}
                    {error && <div className={styles.error}>{error}</div>}

                    {/* Loading */}
                    {loading && (
                        <div className={styles.loading}>
                            <div className={styles.spinner} />
                            <p className={styles.loadingText}>
                                Scraping, analyzing patterns, and generating insights...
                            </p>
                        </div>
                    )}

                    {/* Results */}
                    {result && (
                        <section className={styles.results}>
                            {/* Header */}
                            <div className={styles.resultHeader}>
                                <span className={styles.resultPlatform}>{result.problem_platform}</span>
                                {result.difficulty_assessment?.rating && (
                                    <span className="badge">{result.difficulty_assessment.rating}</span>
                                )}
                                {result.pattern_tags?.map((tag) => (
                                    <span key={tag} className="badge">{tag.replace(/_/g, " ")}</span>
                                ))}
                            </div>
                            <h2 className={styles.resultTitle}>{result.problem_title}</h2>
                            <p className={styles.modelUsed}>
                                Analyzed with <strong>{result.model_used}</strong>
                            </p>

                            {/* Approach Steps */}
                            <div className={styles.resultCard}>
                                <h3>
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--accent)' }}><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z" fill="currentColor" /></svg>
                                    Step-by-Step Approach
                                </h3>
                                <div className={styles.stepList}>
                                    {result.approach.map((step, i) => (
                                        <div key={i} className={styles.step}>
                                            <button
                                                onClick={() => toggleStep(i)}
                                                style={{
                                                    background: "none", border: "none", cursor: "pointer",
                                                    width: "100%", textAlign: "left", color: "inherit",
                                                }}
                                            >
                                                <span className={styles.stepNum}>
                                                    STEP {String(step.step_number).padStart(2, "0")}
                                                </span>
                                                <div className={styles.stepTitle}>{step.title}</div>
                                            </button>
                                            {expandedSteps.has(i) && (
                                                <div className={styles.stepDesc}>
                                                    <p>{step.explanation}</p>
                                                    {step.code_snippet && (
                                                        <div className={styles.codeBlock}>
                                                            <HighlightedCode
                                                                code={step.code_snippet}
                                                                language={result.language || "python"}
                                                            />
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Complexity */}
                            <div className={styles.resultCard}>
                                <h3>
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--accent)' }}><path d="M5 9.2h3V19H5V9.2zM10.6 5h2.8v14h-2.8V5zm5.6 8H19v6h-2.8v-6z" fill="currentColor" /></svg>
                                    Complexity Analysis
                                </h3>
                                <div className={styles.complexityGrid}>
                                    <div className={styles.complexityBox}>
                                        <span className={styles.complexityLabel}>Time Complexity</span>
                                        <span className={styles.complexityValue}>{result.complexity.time}</span>
                                        <p className={styles.complexityReasoning}>{result.complexity.time_reasoning}</p>
                                    </div>
                                    <div className={styles.complexityBox}>
                                        <span className={styles.complexityLabel}>Space Complexity</span>
                                        <span className={styles.complexityValue}>{result.complexity.space}</span>
                                        <p className={styles.complexityReasoning}>{result.complexity.space_reasoning}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Code Solution */}
                            <div className={styles.resultCard}>
                                <h3>
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--accent)' }}><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z" fill="currentColor" /></svg>
                                    Code Solution
                                </h3>
                                {Object.keys(result.code_solutions).length > 1 && (
                                    <div className={styles.tagList} style={{ marginBottom: "var(--space-md)" }}>
                                        {Object.keys(result.code_solutions).map((lang) => (
                                            <button
                                                key={lang}
                                                className={styles.tag}
                                                style={activeCodeLang === lang ? { background: "var(--accent-dim)", color: "var(--accent)", borderColor: "var(--border-accent)" } : {}}
                                                onClick={() => setActiveCodeLang(lang)}
                                            >
                                                {lang}
                                            </button>
                                        ))}
                                    </div>
                                )}
                                <div className={styles.codeBlock}>
                                    <div className={styles.codeBlockHeader}>
                                        <span>{activeCodeLang || Object.keys(result.code_solutions)[0]}</span>
                                        <button
                                            className="btn btn-ghost"
                                            style={{ padding: "4px 10px", fontSize: "0.7rem" }}
                                            onClick={() => {
                                                navigator.clipboard.writeText(
                                                    result.code_solutions[activeCodeLang] ||
                                                    Object.values(result.code_solutions)[0]
                                                );
                                            }}
                                        >
                                            Copy
                                        </button>
                                    </div>
                                    <HighlightedCode
                                        code={result.code_solutions[activeCodeLang] || Object.values(result.code_solutions)[0]}
                                        language={activeCodeLang || Object.keys(result.code_solutions)[0]}
                                    />
                                </div>
                            </div>

                            {/* Key Insights */}
                            {result.key_insights && result.key_insights.length > 0 && (
                                <div className={styles.resultCard}>
                                    <h3>
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--accent)' }}><path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z" fill="currentColor" /></svg>
                                        Key Insights
                                    </h3>
                                    <div className={styles.insightList}>
                                        {result.key_insights.map((insight, i) => (
                                            <div key={i} className={styles.insight}>{insight}</div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Related Problems */}
                            {result.related_problems && result.related_problems.length > 0 && (
                                <div className={styles.resultCard}>
                                    <h3>
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--accent)' }}><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z" fill="currentColor" /></svg>
                                        Related Problems
                                    </h3>
                                    <div className={styles.tagList}>
                                        {result.related_problems.map((rp, i) => (
                                            <a
                                                key={i}
                                                href={rp.url || "#"}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className={styles.tag}
                                                style={{ cursor: "pointer" }}
                                            >
                                                {rp.title} ({rp.platform})
                                            </a>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Interview Tips */}
                            {result.interview_tips && result.interview_tips.length > 0 && (
                                <div className={styles.resultCard}>
                                    <h3>
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--accent)' }}><path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z" fill="currentColor" /></svg>
                                        Interview Tips
                                    </h3>
                                    <div className={styles.insightList}>
                                        {result.interview_tips.map((tip, i) => (
                                            <div key={i} className={styles.insight}>{tip}</div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </section>
                    )}
                </div>
            </main>
        </div>
    );
}

export default function SolvePage() {
    return (
        <Suspense>
            <SolveContent />
        </Suspense>
    );
}
