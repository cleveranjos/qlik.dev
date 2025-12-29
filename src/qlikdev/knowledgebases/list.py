from typing import Dict, List

from qlik_sdk import Qlik

from qlikdev.common import add_user_column, iterate_over_next, print_table

DEFAULT_COLUMNS: List[str] = ["id", "name", "ownerId", "contentSummary.effectivePages", "contentSummary.fileSize"]


def list_knowledgebases(client: Qlik, columns: List[str] = DEFAULT_COLUMNS) -> List[Dict]:
    """
    List knowledgebases, sorted by effective pages.
    """
    results: List[Dict] = []
    for page in iterate_over_next(client, "/knowledgebases?limit=100&sort=name", columns):
        if page:
            results.extend(page)
    results.sort(key=lambda x: x.get("contentSummary.effectivePages", 0), reverse=True)
    add_user_column(client, results)
    print_table(results, "contentSummary.effectivePages")
    return results
