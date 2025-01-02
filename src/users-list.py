from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    headers = ["id","subject","status","name"]
    if (config := getConfig()):
        q = Qlik(config)
        a = q.rest(path="/users?limit=100")
        print_table(a.text,headers)
        while (next := check_next(a.text)):
            a = q.rest(path=next['href'])
            print_table(a.text,headers)     
    else:
        logging.error("Configuration could not be loaded.")
