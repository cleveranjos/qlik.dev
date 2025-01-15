from qlik_sdk import Qlik 
from utils.config import getConfig
from utils.helpers import print_table, check_next
import logging, argparse
from json import loads

def main(app_id: str):
    if (config := getConfig()):
        q = Qlik(config) 
        r = q.rest(path=f"/apps/{app_id}/data/metadata")
        if len(r.text) > 0:
            m = loads(r.text)
            print("Reload task metadata:")   
            print(f"            cpu_time_spent_ms:{m['reload_meta']['cpu_time_spent_ms']}")   
            print(f"            cpu_time_spent_ms:{m['reload_meta']['peak_memory_bytes']}")

            print("Tables:")
            for t in m['tables']:
                print(f"    {t['name']} rows:[{t['no_of_rows']}] fields:[{t['no_of_fields']}]")  

            print("Fields:")
            for f in m['fields']:
                print(f"            {f['name']} tables:[{' , '.join(f['src_tables'])}]")  

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--app_id", help="App Id")
    args = parser.parse_args()
    if args.app_id:
        main(args.app_id)
    else:
        logging.error("Usage: python apps-metadata.py --app_id <app_id>")
