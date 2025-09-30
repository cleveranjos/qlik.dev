from qlik_sdk import Qlik
from qlik_sdk.rest import ConnectionException
from utils.config import getConfig
from json import loads
from time import sleep
import argparse
import logging


def stop_task(q: Qlik, project_id: str, task_id: str) -> bool:
    """Stops a running task."""
    logging.info(f"Stopping task {task_id}")
    try:
        q.rest(method="POST", path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/actions/stop")
        return wait_for_task_stop(q, project_id, task_id)
    except ConnectionException as e:
        logging.error(f"Failed to stop task {task_id}: {e}")
        return False


def wait_for_task_stop(q: Qlik, project_id: str, task_id: str) -> bool:
    """Waits for a task to stop."""
    for _ in range(30):
        r = q.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
        task_state = loads(r.text)
        if 'STOPPED' in task_state.get('runReadiness', {}).get('state', ''):
            return True
        sleep(1)
    logging.warning(f"Task {task_id} did not stop in time.")
    return False


def delete_task(q: Qlik, project_id: str, task_id: str) -> bool:
    """Deletes a specific task."""
    logging.info(f"Deleting task {task_id}")
    retries = 6
    while retries > 0:
        try:
            if is_task_running(q, project_id, task_id):
                stop_task(q, project_id, task_id)
            q.rest(method="DELETE", path=f"/data-projects/{project_id}/data-apps/{task_id}")
            logging.info(f"Task {task_id} deleted.")
            return True
        except ConnectionException as e:
            retries -= 1
            logging.warning(f"Failed to delete task {task_id}: {e}, retrying...")
            sleep(10)
        except Exception as e:
            logging.error(f"Unexpected error while deleting task {task_id}: {e}")
            return False
    logging.error(f"Failed to delete task {task_id} after retries.")
    return False


def is_task_running(q: Qlik, project_id: str, task_id: str) -> bool:
    """Checks if a task is running."""
    r = q.rest(path=f"/di-projects/{project_id}/di-tasks/{task_id}/runtime/state")
    task_state = loads(r.text)
    return 'RUNNING' in task_state.get('runReadiness', {}).get('state', '')


def delete_project(q: Qlik, project_id: str) -> bool:
    """Deletes a project."""
    try:
        r = q.rest(method="DELETE", path=f"/data-projects/{project_id}")
        if r.status_code != 200:
            return False
        logging.info(f"Project {project_id} deleted.")
        return True
    except ConnectionException as e:
        logging.error(f"Failed to delete project {project_id}: {e}")
        return False


def process_tasks(q: Qlik, project_id: str) -> bool:
    """Processes and deletes all tasks in a project."""
    r = q.rest(path=f"/di-projects/{project_id}/di-tasks")
    if r.status_code != 200:
        logging.error(f"Failed to retrieve tasks for project {project_id}. Status code: {r.status_code}")
        return False

    tasks = loads(r.text)
    task_types = ['DATAMART', 'TRANSFORM', 'STORAGE', 'QVD_STORAGE', 'LANDING', 'REGISTERED_DATA', 'REPLICATION']
    filtered_tasks = {task_type: [t for t in tasks if t['type'] == task_type] for task_type in task_types}

    success = True
    for task_type, task_list in filtered_tasks.items():
        for task in task_list:
            success = success and delete_task(q, project_id, task['id'])
    return success


def main(project_id: str):
    """Main function to delete all tasks and the project."""
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        return

    q = Qlik(config)
    if not process_tasks(q, project_id):
        logging.warning(f"Error deleting tasks from project {project_id}.")
    if not delete_project(q, project_id):
       logging.warning(f"Project {project_id} could not be fully deleted.")        
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Clean up Qlik data projects.")
    parser.add_argument("-p", "--project_id", required=True, help="Project ID to clean up.")
    args = parser.parse_args()

    main(args.project_id)
