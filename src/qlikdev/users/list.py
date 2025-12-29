from typing import Any, Dict, List, Optional

from qlik_sdk import Qlik

from qlikdev.common import iterate_over_next, print_table

DEFAULT_COLUMNS: List[str] = ["id", "name", "status", "createdAt"]


def fetch_users(client: Qlik, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve active users.
    """
    cols = columns or DEFAULT_COLUMNS
    results: List[Dict[str, Any]] = []
    api_path = "/users?limit=100&filter=status eq 'active'"

    for page in iterate_over_next(client, api_path, cols):
        if page:
            results.extend(page)
    return results


def list_users(client: Qlik, columns: Optional[List[str]] = None) -> None:
    """
    Fetch and print users.
    """
    print_table(fetch_users(client, columns=columns))
