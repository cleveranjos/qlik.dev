"""
This script retrieves and prints a list of users from a Qlik server using the Qlik SDK.
Modules:
    qlik_sdk (Qlik): A module to interact with Qlik server.
    utils.config (getConfig): A module to get configuration settings.
    utils.helpers (print_table, check_next): Helper functions for printing tables and checking for next pages.
    logging: A module for logging information and errors.
Functions:
    main: The main function that sets up logging, retrieves configuration, and fetches user data from Qlik server.
Usage:
    Run this script directly to fetch and print the list of users from the Qlik server.
"""
from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    headers = ["id", "name", "status"]
    if (config := getConfig()):
        q = Qlik(config)
        a = q.rest(path="/users?limit=100&filter%3Dstatus%20eq%20'active'")
        print_table(a.text,headers)
        while (next := check_next(a.text)):
            a = q.rest(path=next['href'])
            print_table(a.text,headers)     
    else:
        logging.error("Configuration could not be loaded.")
