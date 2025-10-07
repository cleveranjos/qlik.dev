"""
datafiles-remove-orphan.py
-----------------

Query Qlik for large data files (QVD/CSV) idientified as orphans (no known owner),

This module:
- Loads API configuration via utils.config.getConfig()
- Queries the /data-files endpoint for *.qvd and *.csv files (paginated)
- Enriches rows with user display names via utils.helpers.add_user_column
- Filter out files with known owners
- Remove files 

Usage:
    python datafiles-remove-orphan.py

Notes:
- iterate_over_next is assumed to yield pages (lists) of file dicts.

"""
from typing import List
from qlik_sdk import Qlik
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next,add_user_column
import logging

# API patterns to collect pages for QVD and CSV files
PATTERNS: List[str] = ["*.qvd", "*.csv"]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        exit(1)
    cols = ["id", "name", "ownerId", "size"]
    q = Qlik(config)
    logging.info("Collecting data files...")
    results = []
    for pattern in PATTERNS:
        for r in iterate_over_next(q, f"/data-files?limit=100&includeAllSpaces=true&includeFolders=true&sort=-size&baseNameWildcard={pattern}", cols):
            results = results + r

    add_user_column(q, results)
    # Filter out known users 
    results = [r for r in results if "Unknown" in r["ownerId"]]
    results.sort(key=lambda x: x.get("size", 0), reverse=True)
    print_table(results, "size")    