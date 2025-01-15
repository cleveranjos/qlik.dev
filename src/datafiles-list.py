from qlik_sdk import Qlik
from utils.config import getConfig
from utils.helpers import print_table, check_next
import logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    headers = ["id", "name", "ownerId", "size", "sum_size"]
    if (config := getConfig()):
        q = Qlik(config)
        a = q.rest(path="/data-files?limit=1000&includeAllSpaces=true&sort=-size&baseNameWildcard=*.qvd")
        grand_total = [0]
        print_table(a.text, headers, "size", grand_total)
        while (next := check_next(a.text)):
            a = q.rest(path=next['href'])
            print_table(a.text, headers, "size", grand_total)
    else:
        logging.error(
            "Configuration could not be loaded. Please check the config file and ensure it is correctly formatted and accessible.")
