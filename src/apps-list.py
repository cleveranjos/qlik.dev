from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next

headers = ["id","name","ownerId","createdAt"]
config = getConfig()
if config:
    q = Qlik(config)
    a = q.rest(path="/items?resourceType=app&limit=100")
    print_table(a.text,headers)
    while (next := check_next(a.text)):
        a = q.rest(path=next['href'])
        print_table(a.text,headers)     
else:
    print("Configuration could not be loaded.")