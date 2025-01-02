
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
from utils.helpers import print_table, shrink_table
import argparse
import logging


def get_status(q: Qlik, project_id: str, task_id: str):
    response = q.rest(
        path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
    if response.status_code != 200:
        return "Not Found"
    response_json = response.json()
    if "runReadiness" not in response_json:
        return "Not Found"
    if "state" not in response_json["runReadiness"]:
        return "Not Found"
    return response_json["runReadiness"]["state"]


def main(project_id: str):
    if (config := getConfig()):
        q = Qlik(config)
        response = q.rest(path=f"/di-projects/{project_id}/di-tasks")
        for t in (d := shrink_table(response.text, ["id", "name", "type"])):
            t['status'] = get_status(q, project_id, t['id'])
        print_table(d, ["id", "name", "type", 'status'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", help="Project Id")
    args = parser.parse_args()
    if args.project_id:
        main(args.project_id)
    else:
        logging.error("Usage: python qcdi-project-list-tasks.py --project_id <project_id>")
