"""
modules/base_scraper.py
-----------------------
Defines the abstract BaseScraper class that all scraper modules must inherit.
Each scraper must implement the methods:
    - fetch(): retrieve HTML or API data
    - parse(): extract relevant information
    - save(): store the processed data
"""

from abc import ABC, abstractmethod


class BaseScraper(ABC):
    @abstractmethod
    def fetch(self):
        """Retrieve data from the target website or API."""
        pass

    @abstractmethod
    def parse(self, html):
        """Parse raw HTML or JSON data and return structured results."""
        pass

    @abstractmethod
    def save(self, data):
        """Save structured data to the local /data directory."""
        pass

    def run(self):
        """Main pipeline combining fetch, parse, and save."""
        html = self.fetch()
        data = self.parse(html)
        self.save(data)
