"""
main.py
-------
Framework entry point.
Loads all scraper modules automatically and runs them.
"""

from modules.registry import load_scrapers
from modules.logger import setup_logger

def main():
    logger = setup_logger()
    scrapers = load_scrapers()

    for scraper in scrapers:
        name = scraper.__class__.__name__
        logger.info(f"Running scraper: {name}")
        try:
            html = scraper.fetch(scraper.list_url)
            data = scraper.parse(html)
            scraper.save(data)
        except Exception as e:
            logger.error(f"Error in {name}: {e}")
        finally:
            scraper._quit_driver()

if __name__ == "__main__":
    main()
