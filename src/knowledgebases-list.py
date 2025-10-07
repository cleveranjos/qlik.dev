from qlik_sdk import Qlik
from utils.config import getConfig
from utils.helpers import print_table,  iterate_over_next, add_user_column
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        exit(1)
    results = []
    q = Qlik(config)
    cols = ["id", "name", "ownerId", "contentSummary.effectivePages", "contentSummary.fileSize"]
    for r in iterate_over_next(q, "/knowledgebases?limit=100&sort=name",cols):
        results = results + r
    results.sort(key=lambda x: x.get("contentSummary.effectivePages", 0), reverse=True)
    add_user_column(q, results)
    print_table(results,"contentSummary.effectivePages")