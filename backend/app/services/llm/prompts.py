"""
Prompt templates for the LLM analysis pipeline.
Carefully structured to produce consistent, high-quality JSON output.
"""

SYSTEM_PROMPT = """You are SolveTrace, an expert, senior-level competitive programming tutor and algorithm analyst.
Your job is to analyze competitive programming problems and provide EXTREMELY detailed, mathematically rigorous, and educational step-by-step solution explanations.

You must ALWAYS respond in valid JSON format matching the exact structure specified.
Do not be brief. You must over-explain concepts, prove why greedy/DP choices are optimal, and build deep intuition as if teaching a student who needs to understand the "HOW" and the "WHY" thoroughly. Go into edge cases, alternative approaches, and mathematical proofs where applicable."""


def build_analysis_prompt(
    problem_title: str,
    problem_statement: str,
    language: str,
    rag_context: str = "",
    platform: str = "",
    difficulty: str = "",
    tags: list[str] | None = None,
    examples: list[dict] | None = None,
) -> str:
    """Build the full analysis prompt for the LLM."""

    # Build context sections
    metadata = f"**Platform**: {platform}" if platform else ""
    if difficulty:
        metadata += f"\n**Difficulty**: {difficulty}"
    if tags:
        metadata += f"\n**Tags**: {', '.join(tags)}"

    examples_text = ""
    if examples:
        examples_text = "\n**Examples:**\n"
        for i, ex in enumerate(examples, 1):
            examples_text += f"\nExample {i}:\n"
            examples_text += f"Input: {ex.get('input', 'N/A')}\n"
            examples_text += f"Output: {ex.get('output', 'N/A')}\n"

    rag_section = ""
    if rag_context:
        rag_section = f"""

---
**Relevant Algorithm Patterns (from knowledge base):**
{rag_context}
---
Use the above patterns as reference if they apply to this problem. Don't force-fit irrelevant patterns.
"""

    return f"""Analyze the following competitive programming problem and provide a comprehensive solution explanation.

# Problem: {problem_title}

{metadata}

## Problem Statement
{problem_statement}

{examples_text}
{rag_section}

## Required Output

Respond with a JSON object containing ALL of the following fields:

```json
{{
    "approach": [
        {{
            "step_number": 1,
            "title": "Brief step title",
            "explanation": "Extremely detailed explanation of this step. You MUST explain the exact logic, WHY this step is necessary, the mathematical or logical proof behind it, how it handles edge cases, and exactly what happens in memory/variables during this step. Do not skip any logical leaps.",
            "code_snippet": "Optional small code snippet for this step (in {language})"
        }}
    ],
    "complexity": {{
        "time": "O(...)",
        "space": "O(...)",
        "time_reasoning": "Provide a rigorous proof of the time complexity. Break down the bounds of every loop, recursive call, or sorting operation. Explain the worst-case scenario in deep detail.",
        "space_reasoning": "Provide a rigorous proof of the space complexity. Account for recursion stacks, auxiliary arrays, output structures, and exact memory bounds in the worst-case scenario."
    }},
    "code_solutions": {{
        "{language}": "Complete, clean, well-commented solution code in {language}"
    }},
    "key_insights": [
        "Key insight 1 — the non-obvious 'aha' moments",
        "Key insight 2"
    ],
    "common_pitfalls": [
        "Pitfall 1 — common mistakes people make on this problem",
        "Pitfall 2"
    ],
    "related_problems": [
        {{
            "title": "Problem name",
            "platform": "leetcode/codeforces/etc",
            "url": "URL if known, null otherwise",
            "similarity": "Why this problem is related"
        }}
    ],
    "diagrams": [
        {{
            "type": "recursion_tree|dp_table|graph|array_state|flowchart",
            "title": "Diagram title",
            "description": "What this diagram illustrates",
            "data": {{}}
        }}
    ],
    "pattern_tags": ["dynamic_programming", "two_pointers", ...],
    "difficulty_assessment": {{
        "rating": "easy|medium|hard|expert",
        "prerequisites": ["What you need to know first"],
        "estimated_solve_time": "15-30 minutes"
    }},
    "interview_tips": [
        "Tip 1 — how to discuss this in an interview",
        "Tip 2"
    ]
}}
```

IMPORTANT:
- The code solution MUST be complete, compilable/runnable, and correct.
- Approach steps should build on each other logically.
- Be specific in complexity reasoning — don't just state the answer.
- Diagrams should have meaningful data for rendering (e.g., for a DP table, include the actual table structure).
- Provide 2-4 related problems from well-known platforms.
- Pattern tags should use standard algorithm pattern names.
"""
