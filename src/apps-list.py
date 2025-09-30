from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next
import logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        exit(1)
    cols = ["id","name","spaceId","ownerId","createdAt"]
    results = []
    for r in iterate_over_next(Qlik(config), "/items?resourceType=app&limit=100",cols):
        results = results + r
    print_table(results)     