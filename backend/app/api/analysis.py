"""
Analysis API routes — the core endpoint for problem analysis.
Open-source version: no auth, no usage limits.
"""

import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.analysis import Analysis
from app.schemas.analysis import AnalyzeRequest
from app.services.analyzer import analyze_problem
from app.config import get_settings

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_200_OK)
async def create_analysis(
    request_body: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Analyze a competitive programming problem.
    Accepts a URL or pasted problem text.
    Optionally accepts a provider and model override.
    """
    try:
        result = await analyze_problem(
            db=db,
            url=request_body.url,
            problem_text=request_body.problem_text,
            language=request_body.language,
            provider=request_body.provider,
            model=request_body.model,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}. Please try again.",
        )

    await db.commit()
    return result


@router.get("/{analysis_id}")
async def get_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a previously generated analysis by ID."""
    from app.models.problem import Problem

    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    problem_result = await db.execute(
        select(Problem).where(Problem.id == analysis.problem_id)
    )
    problem = problem_result.scalar_one_or_none()

    from app.services.analyzer import _format_analysis_response
    return _format_analysis_response(analysis, problem)
