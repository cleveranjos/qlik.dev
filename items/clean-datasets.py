import os
import requests
import json
import time
HOST = 'partner-engineering-saas.us.qlikcloud.com'
key = os.getenv('APIKEY')
key = 'eyJhbGciOiJFUzM4NCIsImtpZCI6IjhkMjRmNzU1LTIyMzgtNDEwYi05MjU0LTZmY2UyNTkzZWRhMCIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiZUVnbkc4eWRIQVdpSnJFaTVuVVdiM1paZHpXS1R2T3MiLCJqdGkiOiI4ZDI0Zjc1NS0yMjM4LTQxMGItOTI1NC02ZmNlMjU5M2VkYTAiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjI1MDNiNGFjNjRhZjYyNTRmNDg4OWMzIn0.fVoyHN-NoS8CLHtHRmWs_kc_okiqEpMlF3JlSoyHPrs2N1GfdrZ9h1cSOq8OsjBq0TXfdo5HNPX5sV28lYkNsdgjWVWEhOaUvm2-J4_TNYixoGqakn-5QkxEnlVhCXdf'


header = {"Authorization": f"Bearer {key}"}


def get_datasets():
    items = []
    link = f"https://{HOST}/api/v1/items?resourceType=dataset&spaceType=personal&spaceId=personal&ownerId=62503b4ac64af6254f4889c3"
    while len(link):
        r = requests.get(link, headers=header)
        if len(r.text) > 0:
            t = json.loads(r.text)
            try:
                items = items + t['data']
                link = t['links']['next']['href']
            except KeyError:
                link = ''
    return items
    ''' Main '''

for item in get_datasets():
    r = requests.delete(f"https://{HOST}/api/v1/qix-datafiles/{item['id']}", headers=header)
    print(r)
