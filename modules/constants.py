"""
modules/constants.py
--------------------
Framework-wide constants for reuse across scrapers and modules.
"""

USER_AGENT = "Mozilla/5.0 (compatible; JobScraper/1.0)" # replace with 
DEFAULT_TIMEOUT = 15
VALID_FETCH_MODES = ["requests", "selenium"]
DATE_FORMAT = "%Y-%m-%d"
RAW_DATA_PATH = "data/raw/"
CLEAN_DATA_PATH = "data/cleaned/"
ARCHIVE_PATH = "data/archive/"
