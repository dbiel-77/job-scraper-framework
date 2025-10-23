"""
scrapers/senate_scraper.py
--------------------------
Scraper for Senate of Canada job postings (VidCruiter platform).

Uses the shared BaseScraper class in Selenium mode for dynamic listings,
and falls back to requests for job detail pages. Regex patterns extract
structured job fields into a clean DataFrame.
"""

import re
import time
import pandas as pd
import requests
from pathlib import Path
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from modules.base_scraper import BaseScraper


class Scraper(BaseScraper):
    def __init__(self):
        # Use selenium mode since the listing page is dynamic
        super().__init__(fetch_mode="selenium", wait_time=3)

        self.base_url = "https://sencanada.hiringplatform.ca"
        self.list_url = f"{self.base_url}/list/CurrentOpportunities"
        self.field_patterns = {
            "directorate": r"Directorate:\s*</strong>\s*([^<]+)",
            "classification": r"Classification:\s*</strong>\s*([^<]+)",
            "employment_type": r"Job Type:\s*</strong>\s*([^<]+)",
            "location": r"Location:\s*</strong>\s*([^<]+)",
            "closing_date": r"Closing Date:\s*</strong>\s*([^<]+)",
        }

    def parse(self, html):
        """
        Parse the job listing page and individual job detail pages.

        Args:
            html (str): Raw HTML of the listing page
        Returns:
            pd.DataFrame: Structured job data
        """
        soup = BeautifulSoup(html, "lxml")
        links = soup.select("h2.vidcruiter-job-item-title a")

        jobs = []
        for link in links:
            title = link.get_text(strip=True)
            href = link.get("href")

            # Normalize relative URLs
            if not href.startswith("http"):
                href = self.base_url + href

            # Fetch the job detail page using requests
            try:
                r = requests.get(href, headers={"User-Agent": "Mozilla/5.0"})
                r.raise_for_status()
                detail_html = r.text
            except Exception as e:
                print(f"Failed to fetch detail page: {href} ({e})")
                continue

            fields = {}
            for key, pattern in self.field_patterns.items():
                match = re.search(pattern, detail_html, re.IGNORECASE)
                if match:
                    fields[key] = match.group(1).strip()

            jobs.append({
                "source": "senate",
                "id": href.split("/")[-1].split("?")[0],
                "title": title,
                "reference": None,
                "department": "Senate of Canada",
                "location": fields.get("location"),
                "url": href,
                "date_posted": None,
                "date_updated": None,
                "employment_type": fields.get("employment_type"),
                "closing_date": fields.get("closing_date"),
                "custom_fields": {
                    "directorate": fields.get("directorate"),
                    "classification": fields.get("classification"),
                },
            })

        return pd.DataFrame(jobs)

    def save(self, data):
        """Save the DataFrame as CSV under /data/raw/."""
        Path("data/raw").mkdir(parents=True, exist_ok=True)
        output = Path("data/raw/senate_jobs.csv")
        data.to_csv(output, index=False)
        print(f"Saved {len(data)} Senate job postings → {output}")
