import argparse
import json
import logging
from pathlib import Path
from typing import Any, Callable, Optional

from qlik_sdk import Qlik

from qlikdev.apps import list_apps, show_metadata
from qlikdev.common import build_config
from qlikdev.datafiles import clean_orphans, list_datafiles, list_orphans
from qlikdev.items import delete_item
from qlikdev.knowledgebases import list_knowledgebases
from qlikdev.qcdi import clean_project, list_projects, list_tasks, stop_running_tasks
from qlikdev.reports.generate import DEFAULT_REPORT, generate_report
from qlikdev.users import list_users


def _client(env_file: Optional[str]) -> Qlik:
    return Qlik(build_config(env_file))


def _add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", help="Path to qlikcloud.env (overrides default search)")
    parser.add_argument("--log-level", default="INFO", help="Logging level (default: INFO)")


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Qlik Cloud helpers CLI")
    _add_common_flags(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    # apps
    apps_parser = subparsers.add_parser("apps", help="App commands")
    apps_sub = apps_parser.add_subparsers(dest="apps_command", required=True)

    apps_list_parser = apps_sub.add_parser("list", help="List apps")
    apps_list_parser.add_argument("--limit", type=int, default=100, help="Items per page")
    apps_list_parser.set_defaults(handler=lambda args, q: list_apps(q, limit=args.limit))

    apps_meta_parser = apps_sub.add_parser("metadata", help="Show app metadata")
    apps_meta_parser.add_argument("--app-id", required=True, help="App ID")
    apps_meta_parser.set_defaults(handler=lambda args, q: show_metadata(q, args.app_id))

    # datafiles
    data_parser = subparsers.add_parser("datafiles", help="Data file commands")
    data_sub = data_parser.add_subparsers(dest="data_command", required=True)

    data_list_parser = data_sub.add_parser("list", help="List data files")
    data_list_parser.add_argument("--pattern", action="append", help="Glob pattern (repeatable)", dest="patterns")
    data_list_parser.add_argument("--limit", type=int, default=100, help="Items per page")
    data_list_parser.add_argument("--no-enrich", action="store_true", help="Skip owner enrichment")
    data_list_parser.set_defaults(
        handler=lambda args, q: list_datafiles(
            q, patterns=args.patterns or None, limit=args.limit, enrich_owners=not args.no_enrich
        )
    )

    data_orphans_parser = data_sub.add_parser("orphans", help="List orphaned data files")
    data_orphans_parser.add_argument("--pattern", action="append", dest="patterns", help="Glob pattern (repeatable)")
    data_orphans_parser.add_argument("--limit", type=int, default=10, help="Max orphaned files to show/delete")
    data_orphans_parser.add_argument("--delete", action="store_true", help="Delete orphaned files")
    data_orphans_parser.set_defaults(
        handler=lambda args, q: clean_orphans(
            q, patterns=args.patterns or None, limit=args.limit, delete=args.delete
        )
    )

    data_clean_parser = data_sub.add_parser("clean-orphans", help="Alias for orphans --delete")
    data_clean_parser.add_argument("--pattern", action="append", dest="patterns", help="Glob pattern (repeatable)")
    data_clean_parser.add_argument("--limit", type=int, default=10, help="Max orphaned files to delete")
    data_clean_parser.set_defaults(
        handler=lambda args, q: clean_orphans(q, patterns=args.patterns or None, limit=args.limit, delete=True)
    )

    # items
    items_parser = subparsers.add_parser("items", help="Catalog item commands")
    items_sub = items_parser.add_subparsers(dest="items_command", required=True)

    item_delete_parser = items_sub.add_parser("delete", help="Delete an item")
    item_delete_parser.add_argument("--id", required=True, help="Item ID")
    item_delete_parser.set_defaults(handler=lambda args, q: delete_item(q, args.id))

    # qcdi
    qcdi_parser = subparsers.add_parser("qcdi", help="Data Integration commands")
    qcdi_sub = qcdi_parser.add_subparsers(dest="qcdi_command", required=True)

    qcdi_projects_parser = qcdi_sub.add_parser("projects", help="List DI projects")
    qcdi_projects_parser.set_defaults(handler=lambda args, q: list_projects(q))

    qcdi_tasks_parser = qcdi_sub.add_parser("tasks", help="List tasks for a project")
    qcdi_tasks_parser.add_argument("--project-id", required=True)
    qcdi_tasks_parser.set_defaults(handler=lambda args, q: list_tasks(q, args.project_id))

    qcdi_stop_parser = qcdi_sub.add_parser("stop-tasks", help="Stop running tasks for a project")
    qcdi_stop_parser.add_argument("--project-id", required=True)
    qcdi_stop_parser.set_defaults(handler=lambda args, q: stop_running_tasks(q, args.project_id))

    qcdi_clean_parser = qcdi_sub.add_parser("clean", help="Delete tasks and a project")
    qcdi_clean_parser.add_argument("--project-id", required=True)
    qcdi_clean_parser.set_defaults(handler=lambda args, q: clean_project(q, args.project_id))

    # knowledgebases
    kb_parser = subparsers.add_parser("knowledgebases", help="Knowledgebase commands")
    kb_sub = kb_parser.add_subparsers(dest="kb_command", required=True)
    kb_list_parser = kb_sub.add_parser("list", help="List knowledgebases")
    kb_list_parser.set_defaults(handler=lambda args, q: list_knowledgebases(q))

    # reports
    reports_parser = subparsers.add_parser("reports", help="Report commands")
    reports_sub = reports_parser.add_subparsers(dest="reports_command", required=True)
    reports_generate_parser = reports_sub.add_parser("generate", help="Generate a report")
    reports_generate_parser.add_argument("--definition", type=Path, help="Path to a JSON report definition")
    reports_generate_parser.add_argument("--output", type=Path, default=Path("report.pdf"), help="Output PDF path")
    reports_generate_parser.set_defaults(
        handler=lambda args, q: generate_report(
            q,
            json.loads(args.definition.read_text()) if args.definition else DEFAULT_REPORT,
            output_path=args.output,
        )
    )

    # users
    users_parser = subparsers.add_parser("users", help="User commands")
    users_sub = users_parser.add_subparsers(dest="users_command", required=True)
    users_list_parser = users_sub.add_parser("list", help="List active users")
    users_list_parser.set_defaults(handler=lambda args, q: list_users(q))

    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    try:
        client = _client(args.env_file)
    except ValueError as exc:
        logging.error(exc)
        raise SystemExit(1) from exc

    handler: Callable[[Any, Qlik], Any] = getattr(args, "handler", None)
    if handler:
        handler(args, client)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
