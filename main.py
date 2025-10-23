"""
main.py
-------
Framework entry point.
Loads all scraper modules automatically and runs them in sequence.

Each scraper follows this lifecycle:
  fetch() → parse() → save()
"""

import yaml
from datetime import datetime
from modules.registry import load_scrapers
from modules.logger import setup_logger
from modules.exceptions import ScraperError
from modules.constants import RAW_DATA_PATH


# --- Load settings once globally --------------------------------------------
with open("config/settings.yaml", "r", encoding="utf-8") as f:
    SETTINGS = yaml.safe_load(f)


def main():
    logger = setup_logger()
    scrapers = load_scrapers()

    logger.info(f"Discovered {len(scrapers)} scraper(s). Starting run...")

    for scraper in scrapers:
        name = scraper.__class__.__name__
        start_time = datetime.now()
        logger.info(f"Running scraper: {name}")

        try:
            if not hasattr(scraper, "list_url"):
                logger.warning(f"{name} has no list_url defined — skipping.")
                continue

            html = scraper.fetch(scraper.list_url)
            data = scraper.parse(html)
            scraper.save(data)

            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"{name} completed successfully in {elapsed:.2f}s.")

        except ScraperError as e:
            logger.error(f"{name} failed (framework error): {e}")

        except Exception as e:
            # Catch-all for any unexpected error type
            logger.exception(f"Unexpected error in {name}: {e}")

        finally:
            # Ensure Selenium driver (if used) always quits cleanly
            scraper._quit_driver()

    logger.info("All scrapers finished.")


if __name__ == "__main__":
    main()
