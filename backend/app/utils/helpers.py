"""
General helper utilities.
"""

import re
from urllib.parse import urlparse


# Platform detection patterns
PLATFORM_PATTERNS = {
    "codeforces": [
        r"codeforces\.com/problemset/problem/",
        r"codeforces\.com/contest/\d+/problem/",
        r"codeforces\.com/gym/\d+/problem/",
    ],
    "leetcode": [
        r"leetcode\.com/problems/",
    ],
    "atcoder": [
        r"atcoder\.jp/contests/.+/tasks/",
    ],
    "hackerrank": [
        r"hackerrank\.com/challenges/",
    ],
}


def detect_platform(url: str) -> str | None:
    """Detect the competitive programming platform from a URL."""
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url):
                return platform
    return None


def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def normalize_url(url: str) -> str:
    """Normalize a URL by removing trailing slashes and query params."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    return f"{parsed.scheme}://{parsed.netloc}{path}"


SUPPORTED_LANGUAGES = [
    "python", "cpp", "java", "javascript", "typescript",
    "go", "rust", "csharp", "kotlin", "swift",
]


def validate_language(language: str) -> str:
    """Validate and normalize a programming language name."""
    lang = language.lower().strip()
    aliases = {
        "c++": "cpp", "c#": "csharp", "js": "javascript",
        "ts": "typescript", "py": "python",
    }
    lang = aliases.get(lang, lang)
    if lang not in SUPPORTED_LANGUAGES:
        return "python"  # Default fallback
    return lang
