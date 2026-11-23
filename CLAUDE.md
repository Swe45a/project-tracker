# project-tracker

A small practice terminal program for tracking client projects.

## Stack
- Python 3, standard library only (no external packages)
- Data is stored in `projects.json` in the project root

## Data model
Each project has:
- `title`
- `client`
- `due_date`: the expected due date (YYYY-MM-DD)
- `owner`

## Features (only these two)
1. Create a project
2. List projects

## Run
python3 tracker.py

## Verify
python3 -m unittest

## Never
- Do not open or read `.env`
- Do not run git commands
- Do not add new dependencies
