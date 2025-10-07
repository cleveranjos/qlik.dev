# qlik.dev — Qlik Cloud Python examples

Lightweight collection of small Python scripts that demonstrate how to interact
with Qlik Cloud via the REST API. The repository is focused on quick examples and
helpers you can reuse when exploring or automating tasks in a Qlik Cloud tenant.

This is an examples repository — it's designed for learning and automation
experimentation, not as a production-ready SDK.

## Contents

- `src/` — example scripts (listing apps, users, data files, QDI projects, etc.)
- `src/utils/` — shared helper utilities (API pagination, printing tables, config)
- `requirements.txt` / `pyproject.toml` — Python dependencies and metadata

## Quickstart

Prerequisites

- Python 3.10+ (a virtual environment is recommended)
- Access to a Qlik Cloud tenant and an API key with sufficient permissions

Install dependencies

```powershell
# from the repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configuration

Create a file named `qlikcloud.env` in `src/` (or in the same directory as the
script you run) with the following variables:

```
QCS_SERVER=https://<your-tenant>.qlikcloud.com
QCS_API_KEY=<your-api-key>
```

The helper `utils/config.py` loads this file and constructs the client
configuration used by the example scripts.

How to run an example

Each script in `src/` is a standalone example. For example, list large data
files (QVD/CSV):

```powershell
cd src
.\.venv\Scripts\python.exe datafiles-list.py
```

Or list users:

```powershell
.\.venv\Scripts\python.exe users-list.py
```

Each script prints a human-friendly table to stdout using the helpers in
`src/utils/helpers.py`.

## Key scripts (examples)

- `apps-list.py` — list apps in the tenant
- `users-list.py` — list users (supports pagination)
- `datafiles-list.py` — find large QVD/CSV files and enrich with owner names
- `qcdi-projects-list.py` — list Qlik Data Integration projects
- `qcdi-project-clean.py` — helper to delete QDI project tasks and projects (use with care)

## Helpers

`src/utils/helpers.py` contains reusable utilities used by the examples:

- `iterate_over_next` — follow API pagination `links.next` and yield pages
- `print_table` — format lists/dicts to a readable table
- `add_user_column` — enrich rows with user display names from the API

If you modify or extend those helpers, add small unit tests where practical.

## Security and safe usage

- Do not commit `qlikcloud.env` or any API keys to version control. Add it to
	`.gitignore` if you store it in the project folder during development.
- These scripts may perform destructive actions (see `qcdi-project-clean.py`).
	Always review the code and test in a non-production tenant before running
	destructive operations.

## Contributing

Contributions are welcome. Keep changes small and focused. When adding new
examples, include a brief usage section in the script's module docstring.

1. Fork the repository
2. Add your change and tests (if applicable)
3. Open a pull request describing the change

## License

MIT — see the `LICENSE` file in the repository root for details.

## Contact

Open an issue in this repository if you need help or want to suggest examples to
add.

---

Small, well-documented examples are more valuable than large monoliths. 
