import logging
import time
from typing import Any, Dict, List, Optional

from qlik_sdk import Qlik

from qlikdev.common import iterate_over_next, print_table, shrink_table

DEFAULT_COLUMNS: List[str] = ["id", "name", "type", "status"]


def list_tasks(client: Qlik, project_id: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    List tasks for a given DI project.
    """
    cols = columns or DEFAULT_COLUMNS
    results: List[Dict[str, Any]] = []
    for page in iterate_over_next(client, f"/di-projects/{project_id}/di-tasks", cols):
        if page:
            results.extend(page)
    if not results:
        # Some responses are not paginated; fall back to shrink_table
        response = client.rest(path=f"/di-projects/{project_id}/di-tasks")
        results = shrink_table(response.text, cols)
    print_table(results)
    return results


def _get_status(client: Qlik, project_id: str, task_id: str) -> str:
    response = client.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
    if response.status_code != 200:
        return "Not Found"
    data = response.json()
    return data.get("runReadiness", {}).get("state", "Not Found")


def stop_task(client: Qlik, project_id: str, task_id: str, timeout: int = 60) -> None:
    """
    Request a task stop and wait until it is no longer RUNNING.
    """
    logging.info("Stopping task %s", task_id)
    client.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/actions/stop", method="POST")

    elapsed = 0
    while elapsed < timeout:
        if _get_status(client, project_id, task_id) != "RUNNING":
            logging.info("Task %s stopped successfully.", task_id)
            return
        time.sleep(5)
        elapsed += 5

    logging.warning("Task %s did not stop within %s seconds.", task_id, timeout)


def stop_running_tasks(client: Qlik, project_id: str) -> None:
    """
    Stop all tasks in RUNNING state for a project.
    """
    tasks = list_tasks(client, project_id, columns=DEFAULT_COLUMNS)
    for task in tasks:
        if "RUNNING" in str(task.get("status", "")):
            stop_task(client, project_id, task.get("id"))
