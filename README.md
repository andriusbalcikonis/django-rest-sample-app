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

Clarification: dependencies (virtualenv, pip install, dbs, migrations) will be installed and launched automatically.

**To create superadmin user:**

1. `make createsuperuser`

**To check DB contents via pgadmin**

1. `make`
2. Open http://localhost:8001
