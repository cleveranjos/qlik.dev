from qlik_sdk import Qlik
from utils.config import getConfig
from utils.helpers import print_table, shrink_table
import argparse
import logging
import time


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


def stop_task(q: Qlik, project_id: str, task_id: str):
    logging.info(f"Stopping task {task_id}")
    q.rest(method="POST",
           path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/actions/stop")
    timeout = 60  # total timeout in seconds
    elapsed = 0

    while elapsed < timeout:
        if get_status(q, project_id, task_id) != "RUNNING":
            logging.info(f"Task {task_id} stopped successfully.")
            return None
        time.sleep(10)
        elapsed += 10

    logging.warning(f"Task {task_id} did not stop within the timeout period.")
    return None


def main(project_id: str):
    if (config := getConfig()):
        q = Qlik(config)
        response = q.rest(path=f"/di-projects/{project_id}/di-tasks")
        for t in shrink_table(response.text, ["id"]):
            if "RUNNING" in get_status(q, project_id, t['id']):
                stop_task(q, project_id, t['id'])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", help="Project Id")
    args = parser.parse_args()
    if args.project_id:
        main(args.project_id)
    else:
        logging.error(
            "Usage: python qcdi-project-list-tasks.py --project_id <project_id>")
