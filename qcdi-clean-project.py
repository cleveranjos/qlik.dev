import os
import requests
import json
import time
HOST = 'qcpipelines.us.qlikcloud.com'
HOST = 'partner-engineering-saas.us.qlikcloud.com'
key = os.getenv('APIKEY')
key = 'eyJhbGciOiJFUzM4NCIsImtpZCI6ImI3MTIzMzBkLWE5YzMtNDVjZi1iYmQxLWFkNDczYjQ0ZWJhMyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiUXVpdWdVWndGenZtdTE0XzdDVk9sTV9NczdOcTNnaUQiLCJqdGkiOiJiNzEyMzMwZC1hOWMzLTQ1Y2YtYmJkMS1hZDQ3M2I0NGViYTMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjYzYTM5YTFmYjM2YjdhODYyYjFlMTEzIn0.MzEK4mkGz4aDwVeivlX_NNyPKIm8EyA2UjL8gAtollMF4HD06rr_YrklpnfcuTYzvQiwRZ421C2OjaVFw0gvq6OKluS6XP5tjDU9xYrJLeHR5PeZS-OI_1ElzrK64Hp1'
key = 'eyJhbGciOiJFUzM4NCIsImtpZCI6ImM1ZjgzNTUzLTFmNjItNDJhMy04ZDU0LTcyOWFmZWUyZjE3ZCIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiZUVnbkc4eWRIQVdpSnJFaTVuVVdiM1paZHpXS1R2T3MiLCJqdGkiOiJjNWY4MzU1My0xZjYyLTQyYTMtOGQ1NC03MjlhZmVlMmYxN2QiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjI1MDNiNGFjNjRhZjYyNTRmNDg4OWMzIn0.2eTVQ8srwiytrGUsvzqcNcKN7eCMKok4ihqsQ9QLkjh2K7QBdxnGz9_ELQgn4vEoMQ0JK03Zk35Vn68vOM96ukwg4yt4x6OtkUMtO8kOsa4fazTI634WNp52KDZN78k5'

def delete_task(task_id):
    print(task_id)
    r = requests.get(f"https://{HOST}/api/v1/data-projects/{projectId}/di-tasks/{task_id}/runtime/state",
                     headers={"Authorization": f"Bearer {key}"})
    if len(r.text) > 0:
        t = json.loads(r.text)
        if t['runReadiness']['state'] == 'RUNNING':
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
    r = requests.get(f"https://{HOST}/api/v1/di-projects?spaceId=66465c53f95c5fb2e8b00e7d",
                     headers={"Authorization": f"Bearer {key}"})
    if r.status_code == 200:
        return json.loads(r.text)
    else: 
        return []
    
''' Main '''
for project in ['654d1d1f63630a218ef24531']: # get_projects():
    projectId = project#['id']
    r = requests.get(f"https://{HOST}/api/v1/di-projects/{projectId}/di-tasks",
                     headers={"Authorization": f"Bearer {key}"})
    if r.status_code == 200:
        tasks = json.loads(r.text)
        for type in ['DATAMART', 'TRANSFORM', 'STORAGE', 'LANDING', 'REGISTERED_DATA', 'REPLICATION']:
            for t in [t for t in tasks if t['type'] == type]:
                delete_task(t['id'])
        r = requests.delete(
            f"https://{HOST}/api/v1/data-projects/{projectId}", headers={"Authorization": f"Bearer {key}"})
