"""
modules/job_utils.py
--------------------
Helper utilities shared across scraper modules.
Contains text cleaning, date parsing, and job field normalization tools.
"""

from datetime import datetime
import re


def normalize_whitespace(text: str) -> str:
    """Clean up excessive whitespace and newlines."""
    return re.sub(r"\s+", " ", text).strip()


def parse_date(date_str: str) -> str:
    """Try to parse various date formats and return ISO-style YYYY-MM-DD."""
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date().isoformat()
    except Exception:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
        except Exception:
            return None


def safe_get(element, selector, default=""):
    """Safely extract text from a BeautifulSoup element."""
    try:
        return element.select_one(selector).get_text(strip=True)
    except AttributeError:
        return default
