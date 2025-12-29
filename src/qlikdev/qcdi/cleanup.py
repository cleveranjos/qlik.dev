import logging
from time import sleep
from typing import Dict, List

from qlik_sdk import Qlik
from qlik_sdk.rest import ConnectionException

from qlikdev.common import shrink_table
from qlikdev.qcdi.tasks import stop_task

TASK_TYPES = ["DATAMART", "TRANSFORM", "STORAGE", "QVD_STORAGE", "LANDING", "REGISTERED_DATA", "REPLICATION"]


def _is_task_running(client: Qlik, project_id: str, task_id: str) -> bool:
    response = client.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
    task_state = response.json()
    return "RUNNING" in task_state.get("runReadiness", {}).get("state", "")


def _delete_task(client: Qlik, project_id: str, task_id: str) -> bool:
    """
    Delete a specific task, stopping it first if needed.
    """
    retries = 6
    while retries > 0:
        try:
            if _is_task_running(client, project_id, task_id):
                stop_task(client, project_id, task_id)
            response = client.rest(method="DELETE", path=f"/data-projects/{project_id}/data-apps/{task_id}")
            if response.status_code in (200, 204):
                logging.info("Task %s deleted", task_id)
                return True
            logging.warning("Failed to delete task %s (status %s), retrying...", task_id, response.status_code)
            retries -= 1
            sleep(10)
        except ConnectionException as exc:
            retries -= 1
            logging.warning("Failed to delete task %s: %s, retrying...", task_id, exc)
            sleep(10)
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Unexpected error while deleting task %s: %s", task_id, exc)
            return False
    logging.error("Failed to delete task %s after retries.", task_id)
    return False


def _delete_project(client: Qlik, project_id: str) -> bool:
    response = client.rest(method="DELETE", path=f"/data-projects/{project_id}")
    if response.status_code != 200:
        logging.error("Project %s could not be fully deleted (status %s)", project_id, response.status_code)
        return False
    logging.info("Project %s deleted.", project_id)
    return True


def clean_project(client: Qlik, project_id: str) -> None:
    """
    Stop all tasks in a project, delete them, then delete the project.
    """
    tasks_response = client.rest(path=f"/di-projects/{project_id}/di-tasks")
    tasks: List[Dict] = shrink_table(tasks_response.text, ["id", "type"])
    if not tasks:
        logging.error("No tasks found for project %s (status %s)", project_id, tasks_response.status_code)
        return

    for task_type in TASK_TYPES:
        for task in [t for t in tasks if t.get("type") == task_type]:
            _delete_task(client, project_id, task["id"])

    _delete_project(client, project_id)
