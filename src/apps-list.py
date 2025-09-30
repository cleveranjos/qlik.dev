#!/usr/bin/env python3
"""
List Qlik Cloud Applications

This script retrieves and displays a list of all applications (apps) from a Qlik Cloud 
tenant. It shows essential app information including ID, name, space ID, owner ID, 
and creation date.

The script uses pagination to handle large numbers of apps and formats the output 
in a readable table format. Results are limited to 100 apps per page for optimal 
performance.

Example:
    $ python apps-list.py
"""

from typing import List, Dict, Any
from qlik_sdk import Qlik, Config
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next
import logging
import sys

def fetch_apps(client: Qlik, columns: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieve all applications from Qlik Cloud.
    
    Args:
        client: Authenticated Qlik client instance
        columns: List of app attributes to retrieve
        
    Returns:
        List of dictionaries containing app information
        
    Note:
        Uses pagination with a limit of 100 apps per page
    """
    results = []
    api_path = "/items?resourceType=app&limit=100"
    
    try:
        for page in iterate_over_next(client, api_path, columns):
            if page:
                results.extend(page)
            else:
                logging.warning("Received empty page during app fetch")
        return results
    except Exception as e:
        logging.error(f"Failed to fetch apps: {e}")
        return []

def main() -> None:
    """
    Main function to fetch and display Qlik applications.
    Sets up logging and handles configuration errors.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

    # Initialize Qlik client
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        sys.exit(1)

    # Define app attributes to retrieve
    columns = [
        "id",        # Unique app identifier
        "name",      # App name
        "spaceId",   # ID of containing space
        "ownerId",   # ID of app owner
        "createdAt"  # Creation timestamp
    ]

    # Fetch and display apps
    client = Qlik(config)
    if apps := fetch_apps(client, columns):
        print_table(apps)
    else:
        logging.info("No applications found.")

if __name__ == "__main__":
    main()