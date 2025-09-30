
from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, iterate_over_next
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        exit(1)
    results = []
    q = Qlik(config)
    cols = ["id","name","ownerId","spaceId"]
    for r in iterate_over_next(Qlik(config), "/di-projects",cols):
        results = results + r
    print_table(results)