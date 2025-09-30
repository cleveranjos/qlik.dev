from qlik_sdk import Qlik
from qlik_sdk.rest import ConnectionException
from utils.config import getConfig
import argparse
import logging


def main(item_id: str):
    """Main function to delete an item"""
    if not (config := getConfig()):
        logging.error("Failed to load configuration.")
        return
    try:
        q = Qlik(config)
        q.rest(method="DELETE", path=f"/items/{item_id}")    
    except Exception as e:
        logging.error(f"Failed to delete item: {e}")
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--item_id", help="Item Id")
    args = parser.parse_args()
    if args.item_id:
        main(args.item_id)
    else:
        logging.error("Usage: python items-delete.py --item_id <item_id>")
