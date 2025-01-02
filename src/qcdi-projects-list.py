from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next

headers = ["id","name","ownerId","spaceId"]
config = getConfig()
if config:
    q = Qlik(config)
    a = q.rest(path="/di-projects")
    print_table(a.text,headers)
    while (next := check_next(a.text)):
        a = q.rest(path=next['href'])
        print_table(a.text,headers)     
else:
    print("Configuration could not be loaded.")
