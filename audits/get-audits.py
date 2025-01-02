import os
import requests
import json
import time

HOST = 'partner-engineering-saas.us.qlikcloud.com'
KEY = os.getenv('APIKEY')
KEY = 'eyJhbGciOiJFUzM4NCIsImtpZCI6IjVmMTkxM2JiLWI5NWYtNDFlYy1hNGU3LTBiNjNmOGEyZTM2MiIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiZUVnbkc4eWRIQVdpSnJFaTVuVVdiM1paZHpXS1R2T3MiLCJqdGkiOiI1ZjE5MTNiYi1iOTVmLTQxZWMtYTRlNy0wYjYzZjhhMmUzNjIiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjI1MDNiNGFjNjRhZjYyNTRmNDg4OWMzIn0.eXjRN1mzp_dKgQnEqh7iCqBZl_PgRl7mlsyHW2KymKcXnWRB5LtAzopOYGgNEweaS6K3r0q7-l2dGGmPcIht2FMJpExGgcWixWTD60rUMMDND9NxOOwgKfTAeEei6LyX'
HDR = {"Authorization": f"Bearer {KEY}", "Content-type": "application/json"}

r = requests.get(f"https://{HOST}/api/v1/audits/c024bff449970ec020070882c098d2e7", headers=HDR)
print(r)