"""
Shared helper utilities used by qlikdev commands.
"""

import logging
from json import JSONDecodeError, loads
from typing import Any, Dict, Iterator, List, Optional, Sequence

from qlik_sdk import Qlik
from tabulate import tabulate


def print_table(rows: List[Dict[str, Any]], running_total_column: Optional[str] = None) -> None:
    """
    Pretty-print a list of dict rows as a table.
    """
    if not rows:
        print("(no data)")
        return

    if running_total_column:
        total = 0
        for row in rows:
            value = row.get(running_total_column, 0)
            total += value if isinstance(value, (int, float)) else 0
            row[f"{running_total_column}_total"] = total

    print(tabulate(rows, headers="keys", tablefmt="simple", showindex=True))


def get_nested_value(obj: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Safely retrieve a value from a nested dict using dot notation.
    """
    current = obj
    for key in key_path.split("."):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def return_relative_url(url: str) -> str:
    """
    Extract the path portion after '/v1' in a URL.
    """
    (_, _, path) = url.partition("/v1")
    return path


def add_user_column(q: Qlik, rows: List[Dict[str, Any]], owner_key: str = "ownerId") -> List[Dict[str, Any]]:
    """
    Enrich rows with owner display names using the users endpoint.
    """
    if not rows:
        return []

    user_map: Dict[str, str] = {}
    for page in iterate_over_next(q, "/users?limit=100", ["id", "name"]):
        if page:
            user_map.update({user["id"]: user["name"] for user in page})

    for row in rows:
        owner_id = row.get(owner_key)
        row[owner_key] = f"{owner_id} ({user_map.get(owner_id, 'Unknown')})"

    return rows


def iterate_over_next(
    q: Qlik,
    initial_path: str,
    columns: Optional[List[str]] = None,
) -> Iterator[Optional[List[Dict[str, Any]]]]:
    """
    Follow Qlik's pagination links and yield flattened data pages.
    """
    path = initial_path
    while path:
        try:
            response = q.rest(path=path)
            content = response.text
            if not isinstance(content, str):
                yield None
                break

            data = loads(content)
            payload = data["data"] if isinstance(data, dict) and "data" in data else data
            if isinstance(payload, list):
                yield plainify(payload, columns)

            next_link = data.get("links", {}).get("next", {}).get("href", "") if isinstance(data, dict) else ""
            path = return_relative_url(next_link) if next_link else None
        except (JSONDecodeError, Exception) as exc:
            logging.error("Failed to get or parse data: %s", exc)
            yield None
            break


def plainify(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Flatten rows and optionally filter to a specific column order.
    """
    if not data:
        return []

    selected = columns or list(data[0].keys())
    return [
        {col: get_nested_value(row, col) if "." in col else row.get(col) for col in selected}
        for row in data
    ]


def shrink_table(raw: Any, columns: Sequence[str]) -> List[Dict[str, Any]]:
    """
    Reduce a JSON response (string or object) to a list of dict rows using the provided columns.
    """
    try:
        parsed = loads(raw) if isinstance(raw, str) else raw
    except JSONDecodeError:
        logging.error("Failed to parse response body")
        return []

    if isinstance(parsed, dict) and "data" in parsed:
        parsed = parsed["data"]

    if not isinstance(parsed, list):
        logging.error("Expected a list payload to shrink")
        return []

    return plainify(parsed, list(columns))
