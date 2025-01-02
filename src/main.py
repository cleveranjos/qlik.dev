from qlik_sdk import Auth, AuthType, Config, Qlik, CreateApp, AppAttributes
from qlik_sdk.rpc import RequestObject
from utils.config import getConfig

config = getConfig()
if config:
    q = Qlik(config)
    a = q.rest(path="/items?resourceType=app") 
    print(a.content)
else:
    print("Configuration could not be loaded.")