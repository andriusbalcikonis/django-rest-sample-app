# Django REST sample app

## Intro

This is a simple django rest app, which I built as a job-interview task.

## Requirements

TODO

## Solution

TODO

## Local Development

**Prerequisites**

- Docker
- Docker compose

**First time only setup - to create new admin user**

1. `docker-compose run --rm web ./manage.py createsuperuser`
2. Follow instructions to enter user data

**To start app locally:**

1. `docker-compose up`
2. To see web app, open http://localhost:8000
3. (Optionally) to see the docs, open http://localhost:8001
4. (Optionally) to access db admin, open http://localhost:8002, login with `admin:password` and connect to Main db (password: `postgres`)

**To run any command:**

1. `docker-compose run --rm web ./manage.py [command]`
2. If command created some files in working dir, run `sudo chown -R $USER:$USER .`
