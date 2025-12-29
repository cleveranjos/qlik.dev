
import argparse

from qlikdev.cli import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", required=True, help="Project Id")
    args = parser.parse_args()
    main(["qcdi", "tasks", "--project-id", args.project_id])
      
