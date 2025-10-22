"""
scrapers/example_scraper.py
---------------------------
A minimal example scraper demonstrating the structure expected for new modules.
Replace the URL and parsing logic with real content for your assigned source.
"""

import requests
from bs4 import BeautifulSoup
from modules.base_scraper import BaseScraper
from pathlib import Path
import pandas as pd


class Scraper(BaseScraper):
    def fetch(self):
        url = "https://example.com/jobs"
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse(self, html):
        soup = BeautifulSoup(html, "lxml")
        jobs = []

        for div in soup.find_all("div", class_="job-post"):
            title = div.find("h2").get_text(strip=True)
            company = div.find("span", class_="company").get_text(strip=True)
            jobs.append({"title": title, "company": company})

        return pd.DataFrame(jobs)

    def save(self, data):
        Path("data/raw").mkdir(parents=True, exist_ok=True)
        output_path = Path("data/raw/example_jobs.csv")
        data.to_csv(output_path, index=False)
        print(f"Saved {len(data)} records to {output_path}")
