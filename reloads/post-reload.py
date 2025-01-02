import os
import requests

HOST = 'partner-engineering-saas.us.qlikcloud.com'
KEY = os.getenv('APIKEY')
#KEY = 'eyJhbGciOiJFUzM4NCIsImtpZCI6IjFjZjRjNzU1LTgyNGQtNGM3Zi1iYTNkLWE1MWU3NDZjMDQ5MSIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiZUVnbkc4eWRIQVdpSnJFaTVuVVdiM1paZHpXS1R2T3MiLCJqdGkiOiIxY2Y0Yzc1NS04MjRkLTRjN2YtYmEzZC1hNTFlNzQ2YzA0OTEiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjI1MDNiNGFjNjRhZjYyNTRmNDg4OWMzIn0._uYqWGi-Qb_vIAjOkLfXujZfySCrQZ753L2OfInrz959pVE6Hw7O-DlZHL4d1rNdLUJYugwmupeDdd59YDKpU2exyrpACEcMIJnKDKpSS4_pYODy-WmKWG9Hup4cC56U'
HDR = {"Authorization": f"Bearer {KEY}", "Content-type": "application/json"}

r = requests.post(f"https://{HOST}/api/v1/reloads", headers=HDR,
                  json={"appId": "5ab9e279-db6f-4561-bc81-f3afd7583ba3", "partial": False})
print(r)
