"""
Google Gemini LLM client — wrapper for the Generative AI SDK.
"""

import asyncio
import logging
import google.generativeai as genai
from app.config import get_settings
from app.services.llm.prompts import SYSTEM_PROMPT, build_analysis_prompt
from app.services.llm.parser import parse_llm_response

settings = get_settings()
logger = logging.getLogger(__name__)


class GeminiClient:
    """Wrapper around Google's Generative AI SDK for Gemini models."""

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type="application/json",
            ),
        )

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
        Send a problem to Gemini for analysis and return structured result.
        Runs the synchronous Gemini SDK in a thread pool to avoid blocking.
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

        logger.info(f"Sending analysis request to Gemini for: {problem_title}")

        # Run synchronous Gemini SDK call in thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        try:
            response = await loop.run_in_executor(
                None, self.model.generate_content, prompt
            )
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise ValueError(f"LLM analysis failed: {str(e)}")

        if not response.text:
            # Check for safety blocks
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                raise ValueError(f"Content was blocked by safety filters: {response.prompt_feedback.block_reason}")
            raise ValueError("Empty response from Gemini API")

        logger.info(f"Gemini response received, parsing ({len(response.text)} chars)")

        # Parse the structured output
        return parse_llm_response(response.text)


# Singleton instance
_client: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    """Get or create the Gemini client singleton."""
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
