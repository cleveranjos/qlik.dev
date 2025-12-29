import logging
from typing import Dict, Iterable, List, Optional, Sequence

from qlik_sdk import Qlik

from qlikdev.common import add_user_column, print_table
from qlikdev.datafiles.list import DEFAULT_PATTERNS, fetch_datafiles


def find_orphans(
    client: Qlik,
    patterns: Optional[Iterable[str]] = None,
    limit: int = 50,
) -> List[Dict]:
    """
    Return data files whose owner cannot be resolved (owner is Unknown).
    """
    rows = fetch_datafiles(client, patterns=patterns or DEFAULT_PATTERNS, limit=limit)
    add_user_column(client, rows)
    unknown = [row for row in rows if "Unknown" in str(row.get("ownerId", ""))]
    return unknown[:limit] if limit else unknown


def delete_files(client: Qlik, rows: Sequence[Dict]) -> int:
    """
    Delete data files by ID. Returns count of successful deletions.
    """
    deleted = 0
    for row in rows:
        file_id = row.get("id")
        if not file_id:
            continue
        logging.info("Removing data file [%s - %s]", file_id, row.get("name"))
        response = client.rest(path=f"/data-files/{file_id}", method="DELETE")
        if response.status_code == 204:
            deleted += 1
        else:
            logging.error(
                "Failed to remove data file %s (status %s): %s",
                file_id,
                response.status_code,
                response.text,
            )
    return deleted


def list_orphans(client: Qlik, patterns: Iterable[str] = DEFAULT_PATTERNS, limit: int = 50) -> List[Dict]:
    """
    Print orphaned data files.
    """
    rows = find_orphans(client, patterns=patterns or DEFAULT_PATTERNS, limit=limit)
    print_table(rows, "size")
    return rows


def clean_orphans(
    client: Qlik,
    patterns: Iterable[str] = DEFAULT_PATTERNS,
    limit: int = 10,
    delete: bool = False,
) -> None:
    """
    Show orphaned files and optionally delete them.
    """
    rows = list_orphans(client, patterns=patterns, limit=limit)
    if delete and rows:
        delete_files(client, rows)
