
"""
This script lists tasks for a given Qlik DI project and retrieves their statuses.
Functions:
    get_status(q: Qlik, project_id: str, task_id: str) -> str:
        Retrieves the status of a specific task within a project.
    main(project_id: str):
        Main function that retrieves and prints the list of tasks and their statuses for a given project.
Usage:
    python qcdi-project-list-tasks.py --project_id <project_id>
Arguments:
    -p, --project_id: The ID of the project for which to list tasks.
"""
from qlik_sdk import Qlik
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next
import argparse
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        exit(1)    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", help="Project Id")
    args = parser.parse_args()
    if args.project_id:
        results = []
        cols = ["id", "name", "type", 'status']
        for r in iterate_over_next(Qlik(config), f"/di-projects/{args.project_id}/di-tasks",cols):
            results = results + r 
            print_table(results)  
    else:
        logging.error("Usage: python qcdi-project-list-tasks.py --project_id <project_id>")               
      

