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
    - qlik_sdk
    - utils.config
    - utils.helpers
    - requests
    - json
    - time
    - sys
"""
from utils.config import getConfig
from utils.helpers import print_table, check_next
import sys

def delete_task(task_id):
    print(task_id)
    r = requests.get(f"https://{HOST}/api/v1/data-projects/{projectId}/di-tasks/{task_id}/runtime/state",
                     headers={"Authorization": f"Bearer {key}"})
    if len(r.text) > 0:
        t = json.loads(r.text)
        if t['runReadiness']['state'] == 'RUNNING0':
            print(f"Stopping task {task_id}")
            requests.post(f"https://{HOST}/api/v1/data-projects/{projectId}/di-tasks/{task_id}/runtime/actions/stop",
                          headers={"Authorization": f"Bearer {key}"})
    r = requests.delete(
        f"https://{HOST}/api/v1/data-projects/{projectId}/data-apps/{task_id}",
        headers={"Authorization": f"Bearer {key}"})
    sec = 15
    while sec > 0:
        sec = sec - 1
        time.sleep(1)
        r = requests.get(f"https://{HOST}/api/v1/data-projects/{projectId}/data-apps?filter={task_id}",
                         headers={"Authorization": f"Bearer {key}"})
        t = json.loads(r.text)
        if r.status_code != 200 or len(t['dataApps']) == 0:
            sec = 0

def main():
    print("Hello from the main function!")
    config = getConfig()
    if config:
        q = Qlik(config)
        r = q.rest(path=f"di-projects/{sys.argv[1]}/di-tasks")
        if r.status_code == 200:
            tasks = json.loads(r.text)
            for type in ['DATAMART', 'TRANSFORM', 'STORAGE', 'LANDING', 'REGISTERED_DATA', 'REPLICATION']:
                for t in [t for t in tasks if t['type'] == type]:
                    delete_task(t['id'])
            r = requests.delete(
                f"https://{HOST}/api/v1/data-projects/{projectId}", headers={"Authorization": f"Bearer {key}"})


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print("Usage: python qcdi-clean-project.py <project_id>")        
