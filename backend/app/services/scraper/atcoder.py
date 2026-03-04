"""
AtCoder scraper — extracts problem data from atcoder.jp
"""

import re
import httpx
from bs4 import BeautifulSoup

from app.services.scraper.base import BaseScraper, ProblemData


class AtCoderScraper(BaseScraper):
    """Scraper for AtCoder competitive programming problems."""

    URL_PATTERN = r"atcoder\.jp/contests/([\w-]+)/tasks/([\w-]+)"

    def can_handle(self, url: str) -> bool:
        return bool(re.search(self.URL_PATTERN, url))

    async def scrape(self, url: str) -> ProblemData:
        match = re.search(self.URL_PATTERN, url)
        if not match:
            raise ValueError(f"Cannot parse AtCoder URL: {url}")

        contest_id = match.group(1)
        task_id = match.group(2)

        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            # Try English version first
            headers = {"Accept-Language": "en"}
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title_tag = soup.select_one("span.h2")
        if not title_tag:
            title_tag = soup.select_one("h2")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"
        # Clean prefix like "A - " from title
        title = re.sub(r"^[A-Z]\d?\s*[-–—]\s*", "", title)

        # Extract problem statement
        statement_section = soup.select_one("#task-statement")
        statement = ""
        if statement_section:
            # Get the problem statement (usually in the first section)
            sections = statement_section.select("section")
            statement_parts = []
            for section in sections:
                h3 = section.select_one("h3")
                header = h3.get_text(strip=True) if h3 else ""
                body = section.get_text(strip=True)
                if header:
                    body = body.replace(header, "", 1).strip()
                    statement_parts.append(f"### {header}\n{body}")
                else:
                    statement_parts.append(body)
            statement = "\n\n".join(statement_parts)

        # Extract examples
        examples = self._extract_examples(soup)

        # Extract time/memory limits
        time_limit = None
        memory_limit = None
        limit_section = soup.select_one("#task-statement")
        if limit_section:
            text = limit_section.get_text()
            time_match = re.search(r"Time Limit:\s*(\d+)\s*sec", text)
            mem_match = re.search(r"Memory Limit:\s*(\d+)\s*MB", text)
            if time_match:
                time_limit = f"{time_match.group(1)} sec"
            if mem_match:
                memory_limit = f"{mem_match.group(1)} MB"

        return ProblemData(
            platform="atcoder",
            url=url,
            external_id=task_id,
            title=title,
            statement=statement,
            difficulty=None,  # AtCoder doesn't show difficulty on the page
            tags=None,
            examples=examples if examples else None,
            time_limit=time_limit,
            memory_limit=memory_limit,
        )

    def _extract_examples(self, soup) -> list[dict]:
        """Extract sample input/output from AtCoder problems."""
        examples = []
        pre_tags = soup.select("#task-statement pre")

        # AtCoder alternates input/output in pre tags
        inputs = []
        outputs = []
        for pre in pre_tags:
            # Check the preceding h3 to determine if it's input or output
            prev_h3 = pre.find_previous("h3")
            if prev_h3:
                header = prev_h3.get_text(strip=True).lower()
                if "sample input" in header or "入力例" in header:
                    inputs.append(pre.get_text(strip=True))
                elif "sample output" in header or "出力例" in header:
                    outputs.append(pre.get_text(strip=True))

        for inp, out in zip(inputs, outputs):
            examples.append({"input": inp, "output": out})

        return examples
