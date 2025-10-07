"""
datafiles-remove-orphan.py
-----------------

Query Qlik for large data files (QVD/CSV), enrich results with owner info and
print a sorted table.

This module:
- Loads API configuration via utils.config.getConfig()
- Queries the /data-files endpoint for *.qvd and *.csv files (paginated)
- Enriches rows with user display names via utils.helpers.add_user_column
- Filter out files with known owners
- Sorts results by file size (descending) and prints a formatted table

Usage:
    python datafiles-list-orphan.py

Notes:
- iterate_over_next is assumed to yield pages (lists) of file dicts.
- Adjust PATTERNS to change requested fields or search filters.
- Adjust the LIMIT constant to change the number of orphaned files to display/remove.

"""
from typing import List
from qlik_sdk import Qlik
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next, add_user_column
import logging

# API patterns to collect pages for QVD and CSV files
PATTERNS: List[str] = ["*.csv","*.qvd"]
LIMIT = 10  # Number of orphaned files to display/remove

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
        for r in iterate_over_next(q, f"/data-files?limit={LIMIT}&includeAllSpaces=true&includeFolders=true&sort=-size&baseNameWildcard={pattern}", cols):
            results = results + r

    add_user_column(q, results)
    # Filter out known users
    results = [r for r in results if "Unknown" in r["ownerId"]][:LIMIT]
    results.sort(key=lambda x: x.get("size", 0),reverse=True)  # Sort descending
    print_table(results, "size")
    for r in results:
        logging.info(f"Removing data file [{r['id']} - {r['name']}]")
        try:
            response = q.rest(path=f"/data-files/{r['id']}", method="DELETE")
            if response.status_code != 204:
                logging.error(
                    f"Failed to remove data file: {r['id']} - Status code: {response.status_code} - Response: {response.text}")
                continue
            logging.info(f"Successfully removed data file: {r['id']}")
        except (Exception) as e:
            logging.error(f"Failed remove data file: {{r['id']}} {e}", e)
