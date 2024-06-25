import os
import requests
import json
import time

HOST = 'xxxx.us.qlikcloud.com'
KEY = os.getenv('APIKEY')
HDR = {"Authorization": f"Bearer {KEY}"}



REPORT = {
    "type": "composition-1.0",
    "output": {
        "type": "pdfcomposition",
        "outputId": "composition1",
        "pdfCompositionOutput": {
            "pdfOutputs": [
                {
                    "size": "A4",
                    "align": {
                        "vertical": "middle",
                        "horizontal": "center"
                    },
                    "resizeType": "autofit",
                    "orientation": "A"
                },
                {
                    "size": "A4",
                    "align": {
                        "vertical": "middle",
                        "horizontal": "center"
                    },
                    "resizeType": "autofit",
                    "orientation": "A"
                }
            ]
        }
    },
    "definitions": {
    },
    "compositionTemplates": [
        {
            "type": "sense-sheet-1.0",
            "senseSheetTemplate": {
                "appId": "b92f4d6e-6874-4854-9c82-3d4b6a03f237",
                "sheet": {
                    "id": "9fe59bc4-9584-401b-98e2-0d8b8c593dc8"
                }
            }
        },
        {
            "type": "sense-sheet-1.0",
            "senseSheetTemplate": {
                "appId": "b92f4d6e-6874-4854-9c82-3d4b6a03f237",
                "sheet": {
                    "id": "f0f7b840-717c-491e-8f2e-92909b97f5ff"
                }
            }
        }
    ]
}

r = requests.post(f"https://{HOST}/api/v1/reports", headers=HDR, json=REPORT)

if r.status_code != 202:
    print(r.content)
    exit 

status = r.headers['location']
sec = 60
while sec > 0:
    r = requests.get(status, headers=HDR)
    if r.status_code == 200:
        j = json.loads(r.content)
        if j['status'] in ['failed','aborted','aborting']:
            print(j)
            exit
        if j['status'] == 'done':
            pdf = j['results'][0]['location']
            if len(pdf):
                r = requests.get(pdf,headers=HDR)
                if r.status_code == 200:
                   with open('report.pdf','wb') as file:
                       file.write(r.content)    
            exit 
    sec = sec - 5
    time.sleep(1)
