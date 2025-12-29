import json
import logging
import time
from pathlib import Path
from typing import Dict

from qlik_sdk import Qlik

from qlikdev.common import return_relative_url

DEFAULT_REPORT: Dict = {
    "type": "composition-1.0",
    "output": {
        "type": "pdfcomposition",
        "outputId": "composition1",
        "pdfCompositionOutput": {
            "pdfOutputs": [
                {
                    "size": "A4",
                    "align": {"vertical": "middle", "horizontal": "center"},
                    "resizeType": "autofit",
                    "orientation": "A",
                },
                {
                    "size": "A4",
                    "align": {"vertical": "middle", "horizontal": "center"},
                    "resizeType": "autofit",
                    "orientation": "A",
                },
            ]
        },
    },
    "definitions": {},
    "compositionTemplates": [
        {
            "type": "sense-sheet-1.0",
            "senseSheetTemplate": {
                "appId": "b92f4d6e-6874-4854-9c82-3d4b6a03f237",
                "sheet": {"id": "9fe59bc4-9584-401b-98e2-0d8b8c593dc8"},
            },
        },
        {
            "type": "sense-sheet-1.0",
            "senseSheetTemplate": {
                "appId": "b92f4d6e-6874-4854-9c82-3d4b6a03f237",
                "sheet": {"id": "f0f7b840-717c-491e-8f2e-92909b97f5ff"},
            },
        },
    ],
}


def generate_report(client: Qlik, report: Dict, output_path: Path = Path("report.pdf")) -> None:
    """
    Submit a report request and download the resulting PDF.
    """
    response = client.rest(method="POST", path="/reports", data=report)
    if response.status_code != 202:
        logging.error("Failed to start report: %s", response.content)
        return

    status_path = return_relative_url(response.headers["location"])
    timeout = 60
    while timeout > 0:
        status_response = client.rest(path=status_path)
        if status_response.status_code == 200:
            payload = json.loads(status_response.content)
            status = payload.get("status")
            if status in ["failed", "aborted", "aborting"]:
                logging.error("Report failed: %s", payload)
                return
            if status == "done":
                pdf_path = return_relative_url(payload["results"][0]["location"])
                if not pdf_path:
                    logging.error("No PDF location returned")
                    return
                pdf_response = client.rest(path=pdf_path)
                if pdf_response.status_code == 200:
                    output_path.write_bytes(pdf_response.content)
                    logging.info("Report saved to %s", output_path)
                else:
                    logging.error("Failed to download PDF (status %s)", pdf_response.status_code)
                return
        timeout -= 5
        time.sleep(5)

    logging.warning("Report generation did not complete within timeout.")
