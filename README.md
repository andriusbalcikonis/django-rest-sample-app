# Django REST sample app

## Intro

This is a simple django rest app, which I built as a job-interview task.

## Requirements

TODO

## Solution

TODO

## Local Development

**Prerequisites:**

- Docker
- Docker compose
- Python3 (tested with 3.8.2, possibly works with older versions as well)
- Virtualenv
- Make

**To start application locally:**

1. `make run`
2. Open http://localhost:8000

Clarification: `make run` (or any `make` command) will ensure a few things automatically, before starting the app:

1. Install dependencies (virtualenv, pip install)
2. Perform checks (formatting, linting)
3. Startup local DBs
4. Apply migrations
5. Run tests

**To run checks (linting, formatting) and tests:**

1. `make test`

**To create superadmin user:**

1. `make createsuperuser`

**To check DB contents via pgadmin**

1. `make`
2. Open http://localhost:8001
3. Login with `admin:password` and connect to Main db (password: `postgres`)

**To start debugging:**

Configure and start debugging for your IDE. Details:

- Command before startup: `make`
- Startup command: `env/bin/python manage.py runserver`
- Example configuration for Visual Studio Code is here: `.vscode/launch.json`
