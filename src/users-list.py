"""
List Active Qlik Users

This script retrieves and displays a list of active users from the Qlik platform.
It shows essential user information including ID, name, status, creation date,
and subject identifier.

Usage:
    python users-list.py
"""

from qlik_sdk import Qlik, Config
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next
from typing import List, Dict, Any
import logging
import sys

def get_active_users(client: Qlik, columns: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieve all active users from the Qlik platform.
    
    Args:
        client: Authenticated Qlik client instance
        columns: List of user attributes to retrieve
        
    Returns:
        List of dictionaries containing user information
    """
    results = []
    api_path = "/users?limit=100&filter%3Dstatus%20eq%20'active'"
    
    try:
        for page in iterate_over_next(client, api_path, columns):
            results = results + page
        return results
    except Exception as e:
        logging.error(f"Failed to fetch users: {e}")
        return []

def main() -> None:
    """Set up logging and retrieve active users."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

    # Initialize Qlik client
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        sys.exit(1)

    # Define user attributes to retrieve
    columns = [
        "id",        # Unique identifier
        "name",      # Display name
        "status",    # Account status
        "createdAt", # Creation timestamp
    ]

    # Fetch and display users
    client = Qlik(config)
    if users := get_active_users(client, columns):
        print_table(users)
    else:
        logging.info("No active users found.")

if __name__ == "__main__":
    main()