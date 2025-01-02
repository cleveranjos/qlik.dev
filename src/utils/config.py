from pathlib import Path
from qlik_sdk import Config, AuthType
from dotenv import dotenv_values


def getConfig() -> Config:
    file_dir = Path(__file__).parent.parent
    dotenv_path = Path.joinpath(file_dir, "qlikcloud.env")
    if not Path.exists(dotenv_path):
        print("Missing .env file: " + dotenv_path)
        return None
    env_values = dotenv_values(dotenv_path=dotenv_path)
    host = env_values.get("QCS_SERVER", False)
    api_key = env_values.get("QCS_API_KEY", False)

    if not host or not api_key:
        print("Missing required environment variables in .env file")
        return None

    return Config(host=host, auth_type=AuthType.APIKey, api_key=api_key)