import os
import requests
import json
import time
HOST = 'partner-engineering-saas.us.qlikcloud.com'
key = os.getenv('APIKEY')

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

def get_projects():
    r = requests.get(f"https://{HOST}/api/v1/di-projects",#?spaceId=66465c53f95c5fb2e8b00e7d",
                     headers={"Authorization": f"Bearer {key}"})
    if r.status_code == 200:
        return json.loads(r.text)
    else: 
        return []
    
''' Main '''
for project in get_projects():
    projectId = project['id']
    r = requests.get(f"https://{HOST}/api/v1/di-projects/{projectId}/di-tasks",
                     headers={"Authorization": f"Bearer {key}"})   
    if r.status_code == 200:
        tasks = json.loads(r.text)        
        if len(tasks)==0:
            print(f"{r.status_code} {projectId}")
            r = requests.delete(f"https://{HOST}/api/v1/data-projects/{projectId}", headers={"Authorization": f"Bearer {key}"})
        #for type in ['DATAMART', 'TRANSFORM', 'STORAGE', 'LANDING', 'REGISTERED_DATA', 'REPLICATION']:
            #for t in [t for t in tasks if t['type'] == type]:
            #    delete_task(t['id'])
        #r = requests.delete("https://{HOST}/api/v1/data-projects/{projectId}", headers={"Authorization": f"Bearer {key}"})
