"""
This script lists Qlik DI projects using the Qlik SDK.
Modules:
    qlik_sdk: Provides the Qlik class for interacting with Qlik services.
    utils.config: Provides the getConfig function to load configuration settings.
    utils.helpers: Provides helper functions such as print_table and check_next.
Functions:
    main: The main function that executes the script.
Execution:
    The script retrieves and prints a list of Qlik DI projects, including their id, name, ownerId, and spaceId.
    It handles pagination by checking for the next page and retrieving additional projects if available.
Usage:
    Run the script directly to list Qlik DI projects.
"""
from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next

if __name__ == "__main__":
    headers = ["id","name","ownerId","spaceId"]
    if (config := getConfig()):
        q = Qlik(config)
        a = q.rest(path="/di-projects")
        print_table(a.text,headers)
        while (next := check_next(a.text)):
            a = q.rest(path=next['href'])
            print_table(a.text,headers)     
    else:
        print("Configuration could not be loaded.")
