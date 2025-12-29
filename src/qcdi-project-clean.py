import argparse

from qlikdev.cli import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up Qlik data projects.")
    parser.add_argument("-p", "--project_id", required=True, help="Project ID to clean up.")
    args = parser.parse_args()
    main(["qcdi", "clean", "--project-id", args.project_id])
