/* API service for communicating with the SolveTrace backend */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Generic API fetch wrapper.
 */
async function apiFetch(
    endpoint: string,
    options: RequestInit = {}
): Promise<Response> {
    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers as Record<string, string>),
    };

    return fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
    });
}

/* --- Config --- */

export interface LLMProvider {
    id: string;
    name: string;
    available: boolean;
    description: string;
    models: string[];
}

export interface AppConfig {
    current_provider: string;
    providers: LLMProvider[];
}

export async function getConfig(): Promise<AppConfig> {
    const res = await apiFetch("/api/config");
    if (!res.ok) throw new Error("Failed to get config");
    return res.json();
}

/* --- Analysis --- */

export async function analyzeRequest(
    url: string | null,
    problemText: string | null,
    language: string = "python",
    provider?: string,
    model?: string,
) {
    const res = await apiFetch("/api/analyze", {
        method: "POST",
        body: JSON.stringify({
            url,
            problem_text: problemText,
            language,
            provider: provider || undefined,
            model: model || undefined,
        }),
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(
            typeof err.detail === "string"
                ? err.detail
                : err.detail?.message || "Analysis failed"
        );
    }
    return res.json();
}

export async function getAnalysis(id: number) {
    const res = await apiFetch(`/api/analyze/${id}`);
    if (!res.ok) throw new Error("Analysis not found");
    return res.json();
}
