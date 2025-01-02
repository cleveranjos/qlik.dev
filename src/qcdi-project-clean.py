from qlik_sdk import Qlik
"""
This module provides functionality to delete all tasks from a project using the Qlik API.
Functions:
    delete_task(task_id): Deletes a specific task by its ID.
    main(): Main function that deletes all tasks from specified projects.
Usage:
    Run this module from the command line to delete all tasks from specified projects.
Note:
    Ensure that the configuration and necessary API keys are set up correctly in the utils.config module.
Example:
    python qcdi-clean-project.py
Dependencies:
    - utils.config
    - json
    - time
    - argparse
"""
from utils.config import getConfig
from json import loads
import time
import argparse
import logging


def stop_task(q: Qlik, project_id: str, task_id: str):
    logging.info(f"Stopping task {task_id}")
    q.rest(method="POST",
           path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/actions/stop")
    time.sleep(5)
    return None


def delete_task(q: Qlik, project_id: str, task_id: str):
    logging.info(f"Task ID: {task_id}")
    r = q.rest(
        path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
    if len(r.text) > 0:
        t = loads(r.text)
        if 'RUNNING' in t['runReadiness']['state']:
            stop_task(q, project_id, task_id)
    r = q.rest(method="DELETE",
               path=f"/data-projects/{project_id}/data-apps/{task_id}")


def main(project_id: str):
    if (config := getConfig()):
        q = Qlik(config)
        r = q.rest(path=f"/di-projects/{project_id}/di-tasks")
        if r.status_code == 200:
            tasks = loads(r.text)
            filtered_tasks = {type: [t for t in tasks if t['type'] == type] for type in ['DATAMART', 'TRANSFORM', 'STORAGE', 'QVD_STORAGE', 'LANDING', 'REGISTERED_DATA', 'REPLICATION']}
            for type, task_list in filtered_tasks.items():
                for t in task_list:
                    delete_task(q, project_id, t['id'])
            r = q.rest(method="DELETE", path=f"/data-projects/{project_id}")
            if r.status_code == 200:
                logging.info(f"Project {project_id} deleted.")
            else:
                logging.error(f"Error deleting project {project_id}.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", help="Project Id")
    args = parser.parse_args()
    if args.project_id:
        main(args.project_id)
    else:
        logging.error("Usage: python qcdi-project-clean.py --project_id <project_id>")
