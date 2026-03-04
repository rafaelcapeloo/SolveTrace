"""
Problems API routes — browse cached scraped problems.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.problem import Problem

router = APIRouter()


@router.get("")
async def list_problems(
    platform: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List previously scraped and cached problems."""
    query = select(Problem).offset(offset).limit(min(limit, 100))
    if platform:
        query = query.where(Problem.platform == platform)
    query = query.order_by(Problem.scraped_at.desc())

    result = await db.execute(query)
    problems = result.scalars().all()
    return [
        {
            "id": p.id,
            "platform": p.platform,
            "title": p.title,
            "url": p.url,
            "difficulty": p.difficulty,
            "tags": p.tags,
            "scraped_at": p.scraped_at.isoformat() if p.scraped_at else None,
        }
        for p in problems
    ]
