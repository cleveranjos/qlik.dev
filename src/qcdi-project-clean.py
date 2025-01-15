from qlik_sdk import Qlik
from qlik_sdk.rest import ConnectionException
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
from time import sleep
import argparse
import logging


def stop_task(q: Qlik, project_id: str, task_id: str) -> bool:
    logging.info(f"Stopping task {task_id}")
    try:
        q.rest(method="POST", path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/actions/stop")
        for _ in range(30):
            r = q.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
            t = loads(r.text)
            if 'STOPPED' in t.get('runReadiness', {}).get('state', ''):
                break
            sleep(1)
    except ConnectionException as e:
        logging.error(f"Failed to stop task {task_id}: {e}")
    return False


def delete_task(q: Qlik, project_id: str, task_id: str) -> bool:
    logging.info(f"Task ID: {task_id}")
    retries = 6
    while retries > 0:
        try:
            r = q.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
            if len(r.text) > 0:
                t = loads(r.text)
                if 'RUNNING' in t.get('runReadiness', {}).get('state', ''):
                    stop_task(q, project_id, task_id)
            r = q.rest(method="DELETE",path=f"/data-projects/{project_id}/data-apps/{task_id}")
            sleep(10)
            logging.info(f"Task ID: {task_id} deleted.")
            return True
        except ConnectionException as e:
            retries -= 1
            sleep(10)  
            logging.warning(f"Failed to delete task {task_id}: {e}, trying again.")                    
        except Exception as e:
            logging.error(f"Failed to delete task {task_id}: {e}")
            return False


def main(project_id: str):
    if (config := getConfig()):
        q = Qlik(config)
        r = q.rest(path=f"/di-projects/{project_id}/di-tasks")
        if r.status_code == 200:
            tasks = loads(r.text)
            filtered_tasks = {type: [t for t in tasks if t['type'] == type] for type in [
                'DATAMART', 'TRANSFORM', 'STORAGE', 'QVD_STORAGE', 'LANDING', 'REGISTERED_DATA', 'REPLICATION']}
            sucess = True
            for type, task_list in filtered_tasks.items():
                for t in task_list:
                    sucess = sucess and delete_task(q, project_id, t['id'])
            if sucess:
                try:
                    r = q.rest(method="DELETE",path=f"/data-projects/{project_id}")
                    if r.status_code == 200:
                        logging.info(f"Project {project_id} deleted.")
                    else:
                        logging.error(f"Error deleting project {project_id}.")
                    sleep(5)
                except ConnectionException as e:
                    logging.error(f"Failed to delete task : {e}")
            else:
                logging.warning(f"Error deleting tasks from project {project_id}.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", help="Project Id")
    args = parser.parse_args()
    if args.project_id:
        main(args.project_id)
    else:
        logging.error(
            "Usage: python qcdi-project-clean.py --project_id <project_id>")
