import json
import logging
from typing import Any, Dict, Optional

from qlik_sdk import Qlik


def fetch_metadata(client: Qlik, app_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve reload metadata, tables, and fields for an app.
    """
    response = client.rest(path=f"/apps/{app_id}/data/metadata")
    if response.status_code != 200:
        logging.error("Failed to fetch metadata for app %s (status %s)", app_id, response.status_code)
        return None
    try:
        return json.loads(response.text)
    except json.JSONDecodeError as exc:
        logging.error("Invalid metadata payload for app %s: %s", app_id, exc)
        return None


def show_metadata(client: Qlik, app_id: str) -> None:
    """
    Print a human-readable metadata summary.
    """
    metadata = fetch_metadata(client, app_id)
    if not metadata:
        return

    reload_meta = metadata.get("reload_meta", {})
    print("Reload task metadata:")
    print(f"  cpu_time_spent_ms: {reload_meta.get('cpu_time_spent_ms')}")
    print(f"  peak_memory_bytes: {reload_meta.get('peak_memory_bytes')}")

    print("\nTables:")
    for table in metadata.get("tables", []):
        print(f"  {table.get('name')} rows[{table.get('no_of_rows')}] fields[{table.get('no_of_fields')}]")

    print("\nFields:")
    for field in metadata.get("fields", []):
        sources = field.get("src_tables") or []
        print(f"  {field.get('name')} tables[{', '.join(sources)}]")
