from qlik_sdk import  Qlik
from utils.config import getConfig

config = getConfig()
if config:
    q = Qlik(config)
    a = q.rest(path="/audits/c024bff449970ec020070882c098d2e7") 
    print(a.content)
else:
    print("Configuration could not be loaded.")
