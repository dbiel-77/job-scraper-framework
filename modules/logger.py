"""
modules/logger.py
-----------------
Centralized logging configuration for all scraper modules.
Logs messages to both console and /logs/scraper_run.log.
"""

import logging
from pathlib import Path


def setup_logger():
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("scraper_framework")
    logger.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(logs_dir / "scraper_run.log", encoding="utf-8")
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
