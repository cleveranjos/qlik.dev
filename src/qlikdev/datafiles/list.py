from typing import Dict, Iterable, List, Optional, Sequence

from qlik_sdk import Qlik

from qlikdev.common import add_user_column, iterate_over_next, print_table

DEFAULT_PATTERNS: Sequence[str] = ("*.qvd", "*.csv")
DEFAULT_COLUMNS: List[str] = ["id", "name", "ownerId", "size"]


def fetch_datafiles(
    client: Qlik,
    patterns: Iterable[str] = DEFAULT_PATTERNS,
    limit: int = 100,
    columns: Optional[List[str]] = None,
) -> List[Dict]:
    """
    Collect data files across patterns, sorted by size descending.
    """
    cols = columns or DEFAULT_COLUMNS
    results: List[Dict] = []
    for pattern in patterns:
        api_path = (
            f"/data-files?limit={limit}"
            "&includeAllSpaces=true&includeFolders=true"
            f"&sort=-size&baseNameWildcard={pattern}"
        )
        for page in iterate_over_next(client, api_path, cols):
            if page:
                results.extend(page)
    results.sort(key=lambda x: x.get("size", 0), reverse=True)
    return results


def list_datafiles(
    client: Qlik,
    patterns: Optional[Iterable[str]] = None,
    limit: int = 100,
    enrich_owners: bool = True,
) -> List[Dict]:
    """
    Fetch and print data files.
    """
    rows = fetch_datafiles(client, patterns=patterns or DEFAULT_PATTERNS, limit=limit)
    if enrich_owners:
        add_user_column(client, rows)
    print_table(rows, "size")
    return rows
