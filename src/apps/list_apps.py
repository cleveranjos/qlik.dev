from qlik_sdk import Qlik 
from utils.config import getConfig

config = getConfig()
if config:
    q = Qlik(config)
    a = q.rest(path="/items?resourceType=app") 
    print(a.content)
else:
    print("Configuration could not be loaded.")
