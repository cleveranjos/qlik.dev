from typing import Any, Dict, List, Optional

from qlik_sdk import Qlik

from qlikdev.common import iterate_over_next, print_table

DEFAULT_COLUMNS: List[str] = ["id", "name", "spaceId", "ownerId", "createdAt"]


def fetch_apps(client: Qlik, limit: int = 100, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve applications from Qlik Cloud.
    """
    cols = columns or DEFAULT_COLUMNS
    results: List[Dict[str, Any]] = []
    api_path = f"/items?resourceType=app&limit={limit}"

    for page in iterate_over_next(client, api_path, cols):
        if page:
            results.extend(page)
    return results


def list_apps(client: Qlik, limit: int = 100, columns: Optional[List[str]] = None) -> None:
    """
    Fetch and print application details.
    """
    apps = fetch_apps(client, limit=limit, columns=columns)
    print_table(apps)
