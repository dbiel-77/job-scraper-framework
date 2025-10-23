"""
modules/base_scraper.py
-----------------------
Defines a flexible BaseScraper class that supports two fetching modes:
- "requests"  → Uses requests + BeautifulSoup for static pages
- "selenium"  → Uses headless Chrome for dynamic pages

Usage Example:
--------------
from modules.base_scraper import BaseScraper

class MyScraper(BaseScraper):
    def __init__(self):
        super().__init__(fetch_mode="selenium")  # or "requests"
        self.start_url = "https://example.com/jobs"

    def parse(self, html):
        # implement site-specific parsing here
        ...
"""

import time
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class BaseScraper(ABC):
    def __init__(self, fetch_mode: str = "requests", wait_time: int = 3):
        """
        Initialize the scraper.

        Args:
            fetch_mode (str): "requests" or "selenium"
            wait_time (int): Seconds to wait for dynamic pages (Selenium only)
        """
        self.fetch_mode = fetch_mode.lower()
        self.wait_time = wait_time
        self.driver = None  # only used for Selenium

        if self.fetch_mode not in {"requests", "selenium"}:
            raise ValueError("fetch_mode must be 'requests' or 'selenium'")

        if self.fetch_mode == "selenium":
            self._init_driver()

    # --- Setup / teardown -----------------------------------------------------

    def _init_driver(self):
        """Initialize a headless Chrome WebDriver."""
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def _quit_driver(self):
        """Shut down the Selenium driver cleanly."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    # --- Fetching -------------------------------------------------------------

    def fetch(self, url: str) -> str:
        """
        Retrieve HTML content from a given URL using the selected fetch mode.

        Args:
            url (str): Target URL
        Returns:
            str: Raw HTML text
        """
        if self.fetch_mode == "requests":
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.text

        elif self.fetch_mode == "selenium":
            self.driver.get(url)
            time.sleep(self.wait_time)
            return self.driver.page_source

    # --- Parsing --------------------------------------------------------------

    @abstractmethod
    def parse(self, html: str):
        """Parse HTML into structured data (to be implemented by subclass)."""
        pass

    # --- Saving ---------------------------------------------------------------

    @abstractmethod
    def save(self, data):
        """Save parsed data to disk or database (to be implemented by subclass)."""
        pass

    # --- Run lifecycle --------------------------------------------------------

    def run(self, url: str):
        """High-level convenience wrapper for fetch → parse → save."""
        html = self.fetch(url)
        data = self.parse(html)
        self.save(data)
        self._quit_driver()
