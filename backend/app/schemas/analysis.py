"""
Analysis schemas — request/response models for the analysis pipeline.
"""

from pydantic import BaseModel, Field
from datetime import datetime


class AnalyzeRequest(BaseModel):
    """Request to analyze a competitive programming problem."""
    url: str | None = Field(None, description="Problem URL from Codeforces, LeetCode, AtCoder, or HackerRank")
    problem_text: str | None = Field(None, description="Raw problem text (if pasting directly)")
    language: str = Field("python", description="Programming language for code solutions")
    provider: str | None = Field(None, description="LLM provider override (ollama, gemini, openai)")
    model: str | None = Field(None, description="Model name override")

    def model_post_init(self, __context):
        if not self.url and not self.problem_text:
            raise ValueError("Either 'url' or 'problem_text' must be provided")


class ApproachStep(BaseModel):
    """A single step in the solution approach."""
    step_number: int
    title: str
    explanation: str
    code_snippet: str | None = None


class ComplexityAnalysis(BaseModel):
    """Time and space complexity with reasoning."""
    time: str
    space: str
    time_reasoning: str
    space_reasoning: str


class DiagramData(BaseModel):
    """Diagram description for frontend rendering."""
    type: str
    title: str
    description: str
    data: dict


class RelatedProblem(BaseModel):
    """A related problem recommendation."""
    title: str
    platform: str
    url: str | None = None
    similarity: str


class AnalysisResponse(BaseModel):
    """Full analysis result for a competitive programming problem."""
    id: int
    problem_title: str
    problem_platform: str
    problem_url: str | None = None

    # Core analysis
    approach: list[ApproachStep]
    complexity: ComplexityAnalysis
    code_solutions: dict[str, str]

    # Enhanced insights
    key_insights: list[str] | None = None
    common_pitfalls: list[str] | None = None
    related_problems: list[RelatedProblem] | None = None
    diagrams: list[DiagramData] | None = None
    pattern_tags: list[str] | None = None
    difficulty_assessment: dict | None = None
    interview_tips: list[str] | None = None

    # Meta
    language: str
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True
