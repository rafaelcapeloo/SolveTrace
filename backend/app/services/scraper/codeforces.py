"""
Codeforces scraper — extracts problem data from codeforces.com
"""

import re
import httpx
from bs4 import BeautifulSoup

from app.services.scraper.base import BaseScraper, ProblemData


class CodeforcesScraper(BaseScraper):
    """Scraper for Codeforces competitive programming problems."""

    PATTERNS = [
        r"codeforces\.com/problemset/problem/(\d+)/([A-Z]\d?)",
        r"codeforces\.com/contest/(\d+)/problem/([A-Z]\d?)",
        r"codeforces\.com/gym/(\d+)/problem/([A-Z]\d?)",
    ]

    def can_handle(self, url: str) -> bool:
        return any(re.search(p, url) for p in self.PATTERNS)

    async def scrape(self, url: str) -> ProblemData:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title_tag = soup.select_one("div.problem-statement div.title")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"
        # Remove leading letter+period (e.g., "A. Two Sum" → "Two Sum")
        title = re.sub(r"^[A-Z]\d?\.\s*", "", title)

        # Extract problem ID
        match = None
        for pattern in self.PATTERNS:
            match = re.search(pattern, url)
            if match:
                break
        external_id = f"{match.group(1)}{match.group(2)}" if match else None

        # Extract full problem statement
        statement_div = soup.select_one("div.problem-statement")
        statement = self._extract_statement(statement_div) if statement_div else ""

        # Extract time/memory limits
        time_limit = None
        memory_limit = None
        limits = soup.select("div.problem-statement div.time-limit, div.problem-statement div.memory-limit")
        for limit in limits:
            text = limit.get_text(strip=True)
            if "time" in text.lower():
                time_limit = text.replace("time limit per test", "").strip()
            elif "memory" in text.lower():
                memory_limit = text.replace("memory limit per test", "").strip()

        # Extract examples
        examples = self._extract_examples(soup)

        # Extract tags
        tags = [tag.get_text(strip=True) for tag in soup.select("span.tag-box")]

        # Difficulty rating
        difficulty = None
        diff_tag = soup.select_one("span.tag-box[title='Difficulty']")
        if diff_tag:
            difficulty = diff_tag.get_text(strip=True)

        return ProblemData(
            platform="codeforces",
            url=url,
            external_id=external_id,
            title=title,
            statement=statement,
            difficulty=difficulty,
            tags=tags if tags else None,
            examples=examples if examples else None,
            time_limit=time_limit,
            memory_limit=memory_limit,
        )

    def _extract_statement(self, div) -> str:
        """Extract clean problem statement text from the problem div."""
        # Remove the input/output sections to get just the statement
        parts = []
        for child in div.children:
            if hasattr(child, "get"):
                class_attr = child.get("class", [])
                # Skip metadata divs
                if any(c in class_attr for c in ["header", "time-limit", "memory-limit", "input-file", "output-file"]):
                    continue
            text = child.get_text(strip=True) if hasattr(child, "get_text") else str(child).strip()
            if text:
                parts.append(text)
        return "\n\n".join(parts)

    def _extract_examples(self, soup) -> list[dict]:
        """Extract input/output examples."""
        examples = []
        sample_tests = soup.select("div.sample-test div.input, div.sample-test div.output")

        inputs = []
        outputs = []
        for div in sample_tests:
            pre = div.select_one("pre")
            if pre:
                text = pre.get_text("\n", strip=True)
                if "input" in div.get("class", []):
                    inputs.append(text)
                elif "output" in div.get("class", []):
                    outputs.append(text)

        for inp, out in zip(inputs, outputs):
            examples.append({"input": inp, "output": out})

        return examples
