import json
import os
import urllib3

KEY = os.getenv('apiKey')
HOST = os.getenv('HOST')
http = urllib3.PoolManager()


def lambda_handler(event, context):
    appId = event.get('appId', None)
    if not appId:
        return {'statusCode': 400, 'body': json.dumps('Missing parameter')}
    try:
        response = http.request(
            'POST',
            f"https://{HOST}/api/v1/reloads",
            body=json.dumps({"appId": appId, "partial": False}),
            headers={"Authorization": f"Bearer {KEY}",
                     "Content-type": "application/json"}
        )

        # Check if the request was successful
        if response.status == 200:
            return {'statusCode': 200, 'body': json.dumps(f'Success: {response.data.decode("utf-8")}')}
        else:
            return {'statusCode': response.status, 'body': json.dumps(f'Failed: {response.data.decode("utf-8")}')
                    }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}
