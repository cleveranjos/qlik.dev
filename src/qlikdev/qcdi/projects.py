import logging
from typing import Any, Dict, List, Optional

from qlik_sdk import Qlik

from qlikdev.common import iterate_over_next, print_table

DEFAULT_COLUMNS: List[str] = ["id", "name", "ownerId", "spaceId"]


def fetch_projects(client: Qlik, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve Data Integration projects.
    """
    cols = columns or DEFAULT_COLUMNS
    results: List[Dict[str, Any]] = []
    for page in iterate_over_next(client, "/di-projects", cols):
        if page:
            results.extend(page)
        else:
            logging.warning("Received empty page during project fetch")
    return results


def list_projects(client: Qlik, columns: Optional[List[str]] = None) -> None:
    """
    Print Data Integration projects.
    """
    rows = fetch_projects(client, columns=columns)
    print_table(rows)
