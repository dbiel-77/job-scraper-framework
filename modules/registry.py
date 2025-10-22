"""
modules/registry.py
-------------------
Dynamically discovers scraper modules in /scrapers and loads them.
Each scraper module must define a class named `Scraper` that inherits BaseScraper.
"""

import importlib
import pkgutil
import scrapers


def load_scrapers():
    scrapers_list = []
    for _, module_name, _ in pkgutil.iter_modules(scrapers.__path__):
        module = importlib.import_module(f"scrapers.{module_name}")
        if hasattr(module, "Scraper"):
            scrapers_list.append(module.Scraper())
    return scrapers_list
