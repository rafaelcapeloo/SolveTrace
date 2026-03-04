"""
OpenAI LLM client — GPT models via the OpenAI API.
Drop-in replacement for GeminiClient / OllamaClient.
"""

import logging
from openai import AsyncOpenAI

from app.config import get_settings
from app.services.llm.prompts import SYSTEM_PROMPT, build_analysis_prompt
from app.services.llm.parser import parse_llm_response

settings = get_settings()
logger = logging.getLogger(__name__)


class OpenAIClient:
    """Wrapper around the OpenAI Python SDK for GPT models."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def analyze_problem(
        self,
        problem_title: str,
        problem_statement: str,
        language: str = "python",
        rag_context: str = "",
        platform: str = "",
        difficulty: str = "",
        tags: list[str] | None = None,
        examples: list[dict] | None = None,
    ) -> dict:
        """
        Send a problem to OpenAI for analysis.
        Uses the same interface as GeminiClient and OllamaClient.
        """
        prompt = build_analysis_prompt(
            problem_title=problem_title,
            problem_statement=problem_statement,
            language=language,
            rag_context=rag_context,
            platform=platform,
            difficulty=difficulty,
            tags=tags,
            examples=examples,
        )

        logger.info(f"Sending analysis request to OpenAI ({self.model}) for: {problem_title}")

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                top_p=0.95,
                max_tokens=8192,
                response_format={"type": "json_object"},
            )
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise ValueError(f"LLM analysis failed (OpenAI): {str(e)}")

        text = response.choices[0].message.content
        if not text:
            raise ValueError("Empty response from OpenAI API")

        logger.info(f"OpenAI response received, parsing ({len(text)} chars)")
        return parse_llm_response(text)


# Singleton instance
_client: OpenAIClient | None = None


def get_openai_client() -> OpenAIClient:
    """Get or create the OpenAI client singleton."""
    global _client
    if _client is None:
        _client = OpenAIClient()
    return _client
