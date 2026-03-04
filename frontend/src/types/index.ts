/* TypeScript types for SolveTrace frontend */

export interface ApproachStep {
    step_number: number;
    title: string;
    explanation: string;
    code_snippet?: string;
}

export interface ComplexityAnalysis {
    time: string;
    space: string;
    time_reasoning: string;
    space_reasoning: string;
}

export interface DiagramData {
    type: string;
    title: string;
    description: string;
    data: Record<string, unknown>;
}

export interface RelatedProblem {
    title: string;
    platform: string;
    url?: string;
    similarity: string;
}

export interface AnalysisResult {
    id: number;
    problem_title: string;
    problem_platform: string;
    problem_url?: string;
    approach: ApproachStep[];
    complexity: ComplexityAnalysis;
    code_solutions: Record<string, string>;
    key_insights?: string[];
    common_pitfalls?: string[];
    related_problems?: RelatedProblem[];
    diagrams?: DiagramData[];
    pattern_tags?: string[];
    difficulty_assessment?: {
        rating: string;
        prerequisites: string[];
        estimated_solve_time: string;
    };
    interview_tips?: string[];
    language: string;
    model_used: string;
    created_at: string;
}
