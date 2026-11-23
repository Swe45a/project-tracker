import argparse
import json
import sys
from datetime import datetime

DEFAULT_FILE = "projects.json"


def load_projects(path=DEFAULT_FILE):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_projects(projects, path=DEFAULT_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2)


def _clean(name, value):
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{name} is required and cannot be empty")
    return value


def create_project(title, client, due_date, owner, path=DEFAULT_FILE):
    title = _clean("title", title)
    client = _clean("client", client)
    due_date = _clean("due date", due_date)
    owner = _clean("owner", owner)
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"due date must be in YYYY-MM-DD format, got '{due_date}'")
    project = {"title": title, "client": client, "due_date": due_date, "owner": owner}
    projects = load_projects(path)
    projects.append(project)
    save_projects(projects, path)
    return project


def format_projects(projects):
    if not projects:
        return "No projects yet"
    return "\n".join(
        f"{i}. {p['title']} | client: {p['client']} | due: {p['due_date']} | owner: {p['owner']}"
        for i, p in enumerate(projects, 1)
    )


def list_projects(path=DEFAULT_FILE):
    return load_projects(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple project tracker")
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("create", help="create a project")
    c.add_argument("--title", required=True)
    c.add_argument("--client", required=True)
    c.add_argument("--due", required=True, help="expected due date, YYYY-MM-DD")
    c.add_argument("--owner", required=True)
    sub.add_parser("list", help="list all projects")
    args = parser.parse_args(argv)

    if args.command == "create":
        try:
            p = create_project(args.title, args.client, args.due, args.owner)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"Created project: {p['title']}")
    else:
        print(format_projects(list_projects()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
