# django-rest-sample-app

[![Build Status](https://travis-ci.org/andriusbalcikonis/django-rest-sample-app.svg?branch=master)](https://travis-ci.org/andriusbalcikonis/django-rest-sample-app)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Sample django rest app.. Check out the project's [documentation](http://andriusbalcikonis.github.io/django-rest-sample-app/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
