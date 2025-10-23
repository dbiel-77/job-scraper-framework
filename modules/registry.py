"""
modules/registry.py
-------------------
Automatically loads and instantiates all scraper modules.
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
