from qlik_sdk import Qlik
from qlik_sdk.rest import ConnectionException
from utils.config import getConfig
from utils.helpers import print_table,  iterate_over_next
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        exit(1)
    results = []
    q = Qlik(config)
    cols = ["id", "name", "ownerId", "contentSummary.effectivePages", "contentSummary.fileSize"]
    for r in iterate_over_next(Qlik(config), "/knowledgebases?limit=100&sort=name",cols):
        results = results + r
    results.sort(key=lambda x: x.get("contentSummary.effectivePages", 0), reverse=True)
    print_table(results)