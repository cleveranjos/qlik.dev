import os
from qlik_sdk import Config, AuthType, Apps
from dotenv import dotenv_values


def getConfig() -> Config:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(file_dir, "sense.env")
    if not os.path.exists(dotenv_path):
        print("Missing .env file: " + dotenv_path)
    env_values = dotenv_values(dotenv_path=dotenv_path)
    host = env_values.get("QCS_SERVER", False)
    api_key = env_values.get("QCS_API_KEY", False)

    return Config(host=host, auth_type=AuthType.APIKey, api_key=api_key)

apps = Apps(getConfig())
app = apps.get(appId="b92f4d6e-6874-4854-9c82-3d4b6a03f237")
with app.open():
    infos = app.get_lineage()
    print(infos)
