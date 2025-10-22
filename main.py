from modules.registry import load_scrapers
from modules.logger import setup_logger

"""
main.py
-------
Entry point for the job scraper framework.
Discovers all scrapers under /scrapers, runs each one, and logs progress.
"""

def main():
    logger = setup_logger()
    scrapers = load_scrapers()
    for scraper in scrapers:
        logger.info(f"Running {scraper.__class__.__name__}")
        scraper.run()

if __name__ == "__main__":
    main()
