from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next
import logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    headers = ["id","name","ownerId","createdAt"]
    if (config := getConfig()):
        q = Qlik(config)
        a = q.rest(path="/items?resourceType=app&limit=100")
        print_table(a.text,headers)
        while (next := check_next(a.text)):
            a = q.rest(path=next['href'])
            print_table(a.text,headers)     
    else:
        logging.error("Configuration could not be loaded. Please check the config file and ensure it is correctly formatted and accessible.")
