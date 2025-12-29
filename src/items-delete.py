import argparse

from qlikdev.cli import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--item_id", required=True, help="Item Id")
    args = parser.parse_args()
    main(["items", "delete", "--id", args.item_id])
