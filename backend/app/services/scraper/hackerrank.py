"""
HackerRank scraper — extracts problem data from hackerrank.com
"""

import re
import httpx
from bs4 import BeautifulSoup

from app.services.scraper.base import BaseScraper, ProblemData


class HackerRankScraper(BaseScraper):
    """Scraper for HackerRank coding challenges."""

    URL_PATTERN = r"hackerrank\.com/challenges/([\w-]+)"

    def can_handle(self, url: str) -> bool:
        return bool(re.search(self.URL_PATTERN, url))

    async def scrape(self, url: str) -> ProblemData:
        match = re.search(self.URL_PATTERN, url)
        if not match:
            raise ValueError(f"Cannot parse HackerRank URL: {url}")

        slug = match.group(1)

        # Ensure we're hitting the /problem page
        problem_url = f"https://www.hackerrank.com/challenges/{slug}/problem"

        # HackerRank also has a REST API we can try
        api_url = f"https://www.hackerrank.com/rest/contests/master/challenges/{slug}"

        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            # Try REST API first (more structured data)
            try:
                api_response = await client.get(api_url, headers={
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0",
                })
                if api_response.status_code == 200:
                    return self._parse_api_response(api_response.json(), url, slug)
            except Exception:
                pass  # Fall back to HTML scraping

            # Fallback: scrape HTML
            response = await client.get(problem_url, headers={
                "User-Agent": "Mozilla/5.0",
            })
            response.raise_for_status()

        return self._parse_html(response.text, url, slug)

    def _parse_api_response(self, data: dict, url: str, slug: str) -> ProblemData:
        """Parse the HackerRank REST API response."""
        model = data.get("model", {})

        # Clean HTML from body
        body_html = model.get("body_html", "") or model.get("body", "")
        statement = self._clean_html(body_html)

        # Map difficulty
        difficulty_map = {0: "easy", 1: "easy", 2: "medium", 3: "hard", 4: "expert"}
        diff_score = model.get("difficulty_score", None)
        difficulty = difficulty_map.get(diff_score) if diff_score is not None else model.get("difficulty_name")

        # Tags
        tags = [t.get("name", "") for t in model.get("tag_names", []) if t.get("name")]
        if model.get("track", {}).get("name"):
            tags.insert(0, model["track"]["name"])

        return ProblemData(
            platform="hackerrank",
            url=url,
            external_id=str(model.get("id", slug)),
            title=model.get("name", slug.replace("-", " ").title()),
            statement=statement,
            difficulty=difficulty,
            tags=tags if tags else None,
            examples=None,  # Usually embedded in the statement
            time_limit=None,
            memory_limit=None,
        )

    def _parse_html(self, html: str, url: str, slug: str) -> ProblemData:
        """Fallback HTML parser for HackerRank problems."""
        soup = BeautifulSoup(html, "html.parser")

        # Title
        title_tag = soup.select_one("h1.challenge-view-title, h2.ui-icon-wrap")
        title = title_tag.get_text(strip=True) if title_tag else slug.replace("-", " ").title()

        # Statement
        body = soup.select_one("div.challenge-body-html, div.challenge_problem_statement")
        statement = body.get_text("\n", strip=True) if body else ""

        # Difficulty
        diff_tag = soup.select_one("span.difficulty-label, div.difficulty-block span")
        difficulty = diff_tag.get_text(strip=True).lower() if diff_tag else None

        return ProblemData(
            platform="hackerrank",
            url=url,
            external_id=slug,
            title=title,
            statement=statement,
            difficulty=difficulty,
            tags=None,
            examples=None,
            time_limit=None,
            memory_limit=None,
        )

    def _clean_html(self, html: str) -> str:
        """Convert HTML to clean text."""
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n", strip=True)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
