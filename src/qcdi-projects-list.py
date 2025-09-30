
#!/usr/bin/env python3
"""
List Qlik Cloud Data Integration Projects

This script retrieves and displays a list of all Data Integration projects
from a Qlik Cloud tenant. It shows essential project information including
ID, name, owner ID, and space ID.

The script uses pagination to handle large numbers of projects and formats
the output in a readable table format.

Example:
    $ python qcdi-projects-list.py
"""

from typing import List, Dict, Any
from qlik_sdk import Qlik, Config
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next
import logging
import sys

def fetch_di_projects(client: Qlik, columns: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieve all Data Integration projects from Qlik Cloud.
    
    Args:
        client: Authenticated Qlik client instance
        columns: List of project attributes to retrieve
        
    Returns:
        List of dictionaries containing project information
        
    Note:
        Uses pagination to handle large numbers of projects
    """
    results = []
    try:
        for page in iterate_over_next(client, "/di-projects", columns):
            if page:
                results.extend(page)
            else:
                logging.warning("Received empty page during project fetch")
        return results
    except Exception as e:
        logging.error(f"Failed to fetch projects: {e}")
        return []

def main() -> None:
    """
    Main function to fetch and display Data Integration projects.
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

    # Define project attributes to retrieve
    columns = [
        "id",      # Unique project identifier
        "name",    # Project name
        "ownerId", # ID of project owner
        "spaceId"  # ID of containing space
    ]

    # Fetch and display projects
    client = Qlik(config)
    if projects := fetch_di_projects(client, columns):
        print_table(projects)
    else:
        logging.info("No Data Integration projects found.")

if __name__ == "__main__":
    main()