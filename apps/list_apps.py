import os
from dotenv import dotenv_values

from qlik_sdk import Auth, AuthType, Config, Qlik, CreateApp, AppAttributes
from qlik_sdk.rpc import RequestObject

def getConfig() -> Config:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(file_dir, "sense.env")
    if not os.path.exists(dotenv_path):
        print("Missing .env file: " + dotenv_path)
        return None
    env_values = dotenv_values(dotenv_path=dotenv_path)
    host = env_values.get("QCS_SERVER", False)
    api_key = env_values.get("QCS_API_KEY", False)

    if not host or not api_key:
        print("Missing required environment variables in .env file")
        return None

    return Config(host=host, auth_type=AuthType.APIKey, api_key=api_key)

config = getConfig()
if config:
    q = Qlik(config)
    a = q.rest(path="/items?resourceType=app") 
    print(a.content)
else:
    print("Configuration could not be loaded.")
