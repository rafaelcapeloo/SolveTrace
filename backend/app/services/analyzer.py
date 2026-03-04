"""
Analysis Orchestrator — the core pipeline that ties everything together.
Scrape → Cache Check → RAG → LLM → Store → Return
"""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.problem import Problem
from app.models.analysis import Analysis

logger = logging.getLogger(__name__)
from app.services.scraper.base import ProblemData, BaseScraper
from app.services.scraper.codeforces import CodeforcesScraper
from app.services.scraper.leetcode import LeetCodeScraper
from app.services.scraper.atcoder import AtCoderScraper
from app.services.scraper.hackerrank import HackerRankScraper
from app.services.llm.gemini import get_gemini_client
from app.services.llm.ollama import get_ollama_client
from app.services.llm.openai_client import get_openai_client
from app.services.rag.vectorstore import get_vector_store
from app.utils.helpers import detect_platform, normalize_url, validate_language
from app.config import get_settings

settings = get_settings()


# Registry of all available scrapers
SCRAPERS: list[BaseScraper] = [
    CodeforcesScraper(),
    LeetCodeScraper(),
    AtCoderScraper(),
    HackerRankScraper(),
]


def get_scraper(url: str) -> BaseScraper | None:
    """Find the appropriate scraper for a given URL."""
    for scraper in SCRAPERS:
        if scraper.can_handle(url):
            return scraper
    return None


def _get_llm_client(provider: str | None = None):
    """Get the LLM client for the given provider (or default from config)."""
    provider = provider or settings.LLM_PROVIDER

    if provider == "ollama":
        return get_ollama_client(), settings.OLLAMA_MODEL
    elif provider == "openai":
        return get_openai_client(), settings.OPENAI_MODEL
    else:  # gemini
        return get_gemini_client(), settings.GEMINI_MODEL


async def analyze_problem(
    db: AsyncSession,
    url: str | None = None,
    problem_text: str | None = None,
    language: str = "python",
    provider: str | None = None,
    model: str | None = None,
) -> dict:
    """
    Full analysis pipeline:
    1. Scrape or use provided text
    2. Check cache for existing analysis
    3. Query RAG for relevant patterns
    4. Call LLM for analysis
    5. Store result in database
    6. Return structured analysis
    """
    language = validate_language(language)

    # --- Step 1: Get problem data ---
    problem_data = None
    problem_record = None

    if url:
        url = normalize_url(url)
        logger.info(f"[Step 1] Looking up URL: {url}")

        # Check if problem already exists in DB
        result = await db.execute(select(Problem).where(Problem.url == url))
        problem_record = result.scalar_one_or_none()

        if problem_record:
            # Check for existing analysis in the same language
            existing = await db.execute(
                select(Analysis).where(
                    Analysis.problem_id == problem_record.id,
                    Analysis.language == language,
                )
            )
            existing_analysis = existing.scalar_one_or_none()
            if existing_analysis:
                return _format_analysis_response(existing_analysis, problem_record)

            # Problem exists but no analysis in this language
            problem_data = ProblemData(
                platform=problem_record.platform,
                url=problem_record.url,
                external_id=problem_record.external_id,
                title=problem_record.title,
                statement=problem_record.statement,
                difficulty=problem_record.difficulty,
                tags=problem_record.tags,
                examples=problem_record.examples,
                time_limit=problem_record.time_limit,
                memory_limit=problem_record.memory_limit,
            )
        else:
            # Scrape the problem
            scraper = get_scraper(url)
            if not scraper:
                platform = detect_platform(url)
                raise ValueError(
                    f"Unsupported platform for URL: {url}. "
                    f"Detected: {platform or 'unknown'}. "
                    f"Supported: Codeforces, LeetCode, AtCoder, HackerRank."
                )
            logger.info(f"[Step 1] Scraping with {scraper.__class__.__name__}")
            problem_data = await scraper.scrape(url)
            logger.info(f"[Step 1] Scraped: {problem_data.title}")

            # Cache in database
            problem_record = Problem(
                platform=problem_data.platform,
                url=problem_data.url,
                external_id=problem_data.external_id,
                title=problem_data.title,
                statement=problem_data.statement,
                difficulty=problem_data.difficulty,
                tags=problem_data.tags,
                examples=problem_data.examples,
                time_limit=problem_data.time_limit,
                memory_limit=problem_data.memory_limit,
            )
            db.add(problem_record)
            await db.flush()

    elif problem_text:
        # User pasted the problem directly
        problem_data = ProblemData(
            platform="manual",
            url="",
            title="User-provided problem",
            statement=problem_text,
        )
        problem_record = Problem(
            platform="manual",
            url=f"manual_{hash(problem_text)}",
            title="User-provided problem",
            statement=problem_text,
        )
        db.add(problem_record)
        await db.flush()
    else:
        raise ValueError("Either 'url' or 'problem_text' must be provided")

    # --- Step 2: Query RAG for relevant patterns ---
    logger.info("[Step 2] Querying RAG knowledge base...")
    vector_store = get_vector_store()
    relevant_patterns = vector_store.query(problem_data.statement, n_results=3)
    rag_context = vector_store.format_context(relevant_patterns)
    logger.info(f"[Step 2] Found {len(relevant_patterns)} relevant patterns")

    # --- Step 3: Call LLM ---
    llm, model_name = _get_llm_client(provider)
    if model:
        model_name = model
    logger.info(f"[Step 3] Calling {provider or settings.LLM_PROVIDER} LLM ({model_name})...")

    analysis_data = await llm.analyze_problem(
        problem_title=problem_data.title,
        problem_statement=problem_data.statement,
        language=language,
        rag_context=rag_context,
        platform=problem_data.platform,
        difficulty=problem_data.difficulty or "",
        tags=problem_data.tags,
        examples=problem_data.examples,
    )

    logger.info("[Step 3] LLM analysis complete")

    # --- Step 4: Store analysis in DB ---
    analysis_record = Analysis(
        problem_id=problem_record.id,
        approach=analysis_data.get("approach", []),
        complexity=analysis_data.get("complexity", {}),
        code_solutions=analysis_data.get("code_solutions", {}),
        key_insights=analysis_data.get("key_insights"),
        related_problems=analysis_data.get("related_problems"),
        diagrams=analysis_data.get("diagrams"),
        pattern_tags=analysis_data.get("pattern_tags"),
        difficulty_assessment=analysis_data.get("difficulty_assessment"),
        interview_tips=analysis_data.get("interview_tips"),
        language=language,
        model_used=model_name,
    )
    db.add(analysis_record)
    await db.flush()

    # --- Step 5: Return formatted response ---
    return _format_analysis_response(analysis_record, problem_record)


def _format_analysis_response(analysis: Analysis, problem: Problem) -> dict:
    """Format an analysis + problem into the API response structure."""
    return {
        "id": analysis.id,
        "problem_title": problem.title,
        "problem_platform": problem.platform,
        "problem_url": problem.url if problem.url else None,
        "approach": analysis.approach,
        "complexity": analysis.complexity,
        "code_solutions": analysis.code_solutions,
        "key_insights": analysis.key_insights,
        "common_pitfalls": analysis.key_insights,
        "related_problems": analysis.related_problems,
        "diagrams": analysis.diagrams,
        "pattern_tags": analysis.pattern_tags,
        "difficulty_assessment": analysis.difficulty_assessment,
        "interview_tips": analysis.interview_tips,
        "language": analysis.language,
        "model_used": analysis.model_used,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    }
