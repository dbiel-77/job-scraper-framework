"""
modules/helpers.py
------------------
Utility helpers for common tasks such as date normalization,
user-agent rotation, and safe URL handling.
"""

import random
import re
from datetime import datetime
from modules.constants import USER_AGENT, DATE_FORMAT

USER_AGENTS = [
    USER_AGENT,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]


def get_random_user_agent() -> str:
    """Return a random User-Agent string."""
    return random.choice(USER_AGENTS)


def normalize_date(date_str: str) -> str:
    """
    Attempt to normalize date strings into YYYY-MM-DD format.
    Returns None if parsing fails.
    """
    for fmt in ("%B %d, %Y", "%Y-%m-%d", "%d %B %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime(DATE_FORMAT)
        except Exception:
            continue
    return None


def clean_text(text: str) -> str:
    """Trim whitespace and collapse multiple spaces."""
    return re.sub(r"\s+", " ", text.strip())


def build_full_url(base: str, relative: str) -> str:
    """Join a base and relative path safely."""
    if relative.startswith("http"):
        return relative
    return base.rstrip("/") + "/" + relative.lstrip("/")
