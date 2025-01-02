from qlik_sdk import Qlik
"""
This script generates a PDF report using the Qlik API.
The report is defined by the REPORT dictionary, which specifies the composition, output type, and templates for the report.
Modules:
    qlik_sdk (Qlik): A module to interact with the Qlik API.
    utils.config (getConfig): A module to get configuration settings.
    utils.helpers (return_relative_url): A module to return relative URLs.
    logging: A module for logging information.
    time: A module for time-related functions.
    json: A module for JSON manipulation.
Constants:
    REPORT (dict): A dictionary defining the report composition and templates.
Functions:
    main: The main function that generates the report and handles the response.
Usage:
    Run this script directly to generate a PDF report and save it as 'report.pdf'.
"""
from utils.config import getConfig
from utils.helpers import return_relative_url
import logging
import time
import json

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if (config := getConfig()):
        q = Qlik(config)
        response = q.rest(method="POST", path="/reports",  data=REPORT)

        if response.status_code != 202:
            logging.error(response.content)
            exit()

        status = return_relative_url(response.headers['location'])
        sec = 60
        while sec > 0:
            r = q.rest(path=status)
            if r.status_code == 200:
                j = json.loads(r.content)
                if j['status'] in ['failed', 'aborted', 'aborting']:
                    print(j)
                    exit()
                if j['status'] == 'done':
                    pdf = return_relative_url(j['results'][0]['location'])
                    if len(pdf):
                        r = q.rest(path=pdf)
                        if r.status_code == 200:
                            with open('report.pdf', 'wb') as file:
                                file.write(r.content)
                        else:
                            logging.error(f"Failed to download PDF. Status code: {
                                          r.status_code}")
                    exit()
            sec -= 5
            time.sleep(5)
