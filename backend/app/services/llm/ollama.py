"""
Ollama LLM client — local model inference via the Ollama REST API.
Drop-in replacement for GeminiClient when Gemini quotas are exhausted.
"""

import asyncio
import json
import logging
import httpx

from app.config import get_settings
from app.services.llm.prompts import SYSTEM_PROMPT, build_analysis_prompt
from app.services.llm.parser import parse_llm_response

settings = get_settings()
logger = logging.getLogger(__name__)


class OllamaClient:
    """Wrapper around the Ollama REST API for local LLM inference."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

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
        Send a problem to the local Ollama model for analysis.
        Uses the same interface as GeminiClient.analyze_problem.
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

        logger.info(f"Sending analysis request to Ollama ({self.model}) for: {problem_title}")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.3,
                "top_p": 0.95,
                "top_k": 40,
                "num_predict": 8192,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
        except httpx.ConnectError:
            raise ValueError(
                "Cannot connect to Ollama. Make sure it's running: `ollama serve`"
            )
        except Exception as e:
            logger.error(f"Ollama API call failed: {e}")
            raise ValueError(f"LLM analysis failed (Ollama): {str(e)}")

        result = response.json()
        text = result.get("response", "")

        if not text:
            raise ValueError("Empty response from Ollama")

        logger.info(f"Ollama response received, parsing ({len(text)} chars)")

        return parse_llm_response(text)


# Singleton instance
_client: OllamaClient | None = None


def get_ollama_client() -> OllamaClient:
    """Get or create the Ollama client singleton."""
    global _client
    if _client is None:
        _client = OllamaClient()
    return _client
