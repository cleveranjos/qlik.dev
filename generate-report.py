import os
import requests
import json
import time

HOST = 'partner-engineering-saas.us.qlikcloud.com'
KEY = os.getenv('APIKEY')
KEY = 'eyJhbGciOiJFUzM4NCIsImtpZCI6ImMwN2Y2NGE1LWVhMzktNDMyZC05MDU4LWMwMjk4MzIzNTc3ZiIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiZUVnbkc4eWRIQVdpSnJFaTVuVVdiM1paZHpXS1R2T3MiLCJqdGkiOiJjMDdmNjRhNS1lYTM5LTQzMmQtOTA1OC1jMDI5ODMyMzU3N2YiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjI1MDNiNGFjNjRhZjYyNTRmNDg4OWMzIn0.ofB8gI7HJnFO1MIv4MG3ajIKuqiUEq4puahS3jyLWL00QFOoS0fnF0mxF8Kwxyc3AvjSo2TfaNHNBKC3TMB92HV6h668cXtgR2TfYXCS4v_Pwuf5s3vLEoxKgailxnNN'


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
