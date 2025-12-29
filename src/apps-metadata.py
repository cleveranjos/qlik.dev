import argparse
from qlikdev.cli import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--app_id", required=True, help="App Id")
    args = parser.parse_args()
    main(["apps", "metadata", "--app-id", args.app_id])
