import logging
from typing import Optional

from qlik_sdk import Qlik


def delete_item(client: Qlik, item_id: str) -> Optional[bool]:
    """
    Delete a catalog item by ID.
    """
    response = client.rest(method="DELETE", path=f"/items/{item_id}")
    if response.status_code not in (200, 204):
        logging.error("Failed to delete item %s (status %s): %s", item_id, response.status_code, response.text)
        return False
    logging.info("Item %s deleted", item_id)
    return True
