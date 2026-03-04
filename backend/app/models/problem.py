"""
Problem model — cached scraped problems from competitive programming platforms.
"""

from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Source identification
    platform: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # codeforces, leetcode, atcoder, hackerrank
    url: Mapped[str] = mapped_column(String(500), unique=True, index=True, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Platform-specific problem ID

    # Problem content
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tags: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # ["dp", "greedy", "graph"]

    # Input/output examples
    examples: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # [{"input": "...", "output": "..."}]

    # Constraints
    time_limit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    memory_limit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Meta
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    analyses = relationship("Analysis", back_populates="problem", lazy="selectin")
