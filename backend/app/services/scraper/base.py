"""
Base scraper interface — all platform scrapers must implement this.
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel


class ProblemData(BaseModel):
    """Standardized problem data extracted from any platform."""
    platform: str
    url: str
    external_id: str | None = None
    title: str
    statement: str
    difficulty: str | None = None
    tags: list[str] | None = None
    examples: list[dict] | None = None  # [{"input": "...", "output": "..."}]
    time_limit: str | None = None
    memory_limit: str | None = None


class BaseScraper(ABC):
    """Abstract base class for all platform scrapers."""

    @abstractmethod
    async def scrape(self, url: str) -> ProblemData:
        """Scrape a problem from the given URL and return structured data."""
        ...

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Check if this scraper can handle the given URL."""
        ...
