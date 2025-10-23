"""
modules/exceptions.py
---------------------
Custom exception classes to standardize scraper error handling.
"""

class ScraperError(Exception):
    """Base exception for all scraper-related issues."""
    pass


class ScraperTimeoutError(ScraperError):
    """Raised when a request or Selenium call exceeds timeout."""
    pass


class ParseError(ScraperError):
    """Raised when HTML or data parsing fails."""
    pass


class InvalidResponseError(ScraperError):
    """Raised when a response status or structure is invalid."""
    pass


class SaveError(ScraperError):
    """Raised when data cannot be written to disk."""
    pass
