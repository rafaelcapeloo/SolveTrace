"""
Analysis model — LLM-generated solution explanations for problems.
"""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # References
    problem_id: Mapped[int] = mapped_column(Integer, ForeignKey("problems.id"), nullable=False)

    # Analysis content (structured JSON from LLM)
    approach: Mapped[dict] = mapped_column(JSON, nullable=False)
    complexity: Mapped[dict] = mapped_column(JSON, nullable=False)
    code_solutions: Mapped[dict] = mapped_column(JSON, nullable=False)
    key_insights: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    related_problems: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    diagrams: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    pattern_tags: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    difficulty_assessment: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    interview_tips: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Generation metadata
    language: Mapped[str] = mapped_column(String(20), default="python")
    model_used: Mapped[str] = mapped_column(String(50), default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    problem = relationship("Problem", back_populates="analyses")
