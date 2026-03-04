"""
LeetCode scraper — uses LeetCode's public GraphQL API.
"""

import re
import httpx

from app.services.scraper.base import BaseScraper, ProblemData


class LeetCodeScraper(BaseScraper):
    """Scraper for LeetCode problems via their GraphQL API."""

    GRAPHQL_URL = "https://leetcode.com/graphql"
    URL_PATTERN = r"leetcode\.com/problems/([\w-]+)"

    def can_handle(self, url: str) -> bool:
        return bool(re.search(self.URL_PATTERN, url))

    async def scrape(self, url: str) -> ProblemData:
        # Extract slug from URL
        match = re.search(self.URL_PATTERN, url)
        if not match:
            raise ValueError(f"Cannot extract problem slug from URL: {url}")
        slug = match.group(1).rstrip("/")

        # Query LeetCode's GraphQL API
        query = """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                content
                difficulty
                topicTags {
                    name
                    slug
                }
                hints
                exampleTestcaseList
                sampleTestCase
            }
        }
        """

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                self.GRAPHQL_URL,
                json={"query": query, "variables": {"titleSlug": slug}},
                headers={
                    "Content-Type": "application/json",
                    "Referer": "https://leetcode.com",
                },
            )
            response.raise_for_status()

        data = response.json()
        question = data.get("data", {}).get("question")
        if not question:
            raise ValueError(f"Problem not found: {slug}")

        # Extract tags
        tags = [tag["name"] for tag in (question.get("topicTags") or [])]

        # Clean HTML from statement
        statement = self._clean_html(question.get("content", ""))

        # Map difficulty
        difficulty = question.get("difficulty", "").lower()

        return ProblemData(
            platform="leetcode",
            url=f"https://leetcode.com/problems/{slug}/",
            external_id=question.get("questionId"),
            title=question.get("title", "Unknown"),
            statement=statement,
            difficulty=difficulty,
            tags=tags if tags else None,
            examples=None,  # Embedded in the statement HTML
            time_limit=None,
            memory_limit=None,
        )

    def _clean_html(self, html: str) -> str:
        """Convert HTML content to readable text."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Replace <code> with backticks
        for code in soup.find_all("code"):
            code.string = f"`{code.get_text()}`"

        # Replace <strong> with **
        for strong in soup.find_all(["strong", "b"]):
            strong.string = f"**{strong.get_text()}**"

        # Replace <em> with *
        for em in soup.find_all(["em", "i"]):
            em.string = f"*{em.get_text()}*"

        # Replace <pre> with code blocks
        for pre in soup.find_all("pre"):
            pre.string = f"\n```\n{pre.get_text()}\n```\n"

        text = soup.get_text("\n", strip=True)
        # Clean up excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
