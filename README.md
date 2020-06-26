# Django REST sample app

## Overview

This is a simple django rest app, which I built as an excersize.

## Quickstart

**Prerequisites:**

- Docker
- Docker compose

**To run application:**

1. `docker-compose up`
2. Open http://localhost:8010

## Excercize requirements

**About**

Restaurant task

Company needs internal service for its’ employees which helps them to make a decision on lunch place.
Each restaurant will be uploading menus using the system every day over API and employees will vote for menu before leaving for lunch.
The solution can be presented in Docker environment, which will add additional Karma points.

**Requirements for implementation**

1. There should be an API for:

- Authentication
- Creating restaurant
- Uploading menu for restaurant (There should be a menu for each day)
- Creating employee
- Getting current day menu
- Voting for restaurant menu
- Getting results for current day. The winner restaurant should not be the winner for
- 3 consecutive working days
- Logout

2. Reasonable amount of automated tests
3. Solution should be uploaded to version control
4. Solution should be built using: Django and Python3, Django Rest Framework, SQL database of your choice (PostgreSQL, SQLite, MySQL, etc)
5. Sufficient logging must be implemented
6. PEP8 rules must be followed. Additional linters are welcomed (PyLint, etc)
7. Project README.md must be created with launch instructions

## Solution

**Functionality design**

In real world, this would be clarified with PO or clients. This is an excersize, so I just made following assumptons:

1. Admin users are created with script and cannot be created other ways.
2. Any anonymous user can register and then login.
3. When newly registered user log's in, it can update his profile details - first name and last name.
4. Newly register user can not do anything else, until it's approved by admin to represent restaurant and/or organization.
5. Admins approve users by finding and updating user details in admins user list.
6. Restaurant representing users can upload restaurant todays menu, change it and delete it, but only that day and only one menu per day (previous will be overwritten).
7. Organization users can see todays voting options.
8. Todays voting stats are displayed for everyone in the same view as their voting options. They are calculated only for their organization scope.
9. When calculating "three consecutive days winner not allowed" rule, system will assume working days are Monday till Friday (no custom holiday calendar check for now).there
10. If there are no votes, there is no winner menu that day.
11. If there are equal amount of votes, winner menu will be the one, which had first vote that day
12. Organization users can post todays vote, but only one vote per day (previous will be overwritten).
13. Organization users can see list of all their previous votes (not only todays), and delete any of their votes, if they wish.

**API design**

| Endpoint                       | HTTP method | Action                                                           | Allowed for users              |
| :----------------------------- | :---------- | :--------------------------------------------------------------- | :----------------------------- |
| my-user                        | POST        | Create new user                                                  | Anonymous                      |
| my-user                        | GET         | Get my user profile (will see represented restaurant and/or org) | Any user                       |
| my-user                        | PUT         | Update my user profile details                                   | Any user                       |
| my-user                        | DELETE      | Delete my user                                                   | Any user                       |
| my-restaurant-todays-menu      | GET         | Get todays menu list (always only one item)                      | User representing restaurant   |
| my-restaurant-todays-menu      | POST        | Upload todays menu (will override if repeated upload today)      | User representing restaurant   |
| my-restaurant-todays-menu/[id] | GET         | Get todays menu                                                  | User representing restaurant   |
| my-restaurant-todays-menu/[id] | PUT         | Update todays menu                                               | User representing restaurant   |
| my-restaurant-todays-menu/[id] | DELETE      | Delete todays menu                                               | User representing restaurant   |
| my-organization-voting-results | GET         | Voting results inside my organization                            | User representing organization |
| my-todays-options              | GET         | Lists todays vote options and stats                              | User representing organization |
| my-votes                       | GET         | Get all my previous votes                                        | User representing organization |
| my-votes                       | POST        | Post my vote for today (will override if repeated vote today)    | User representing organization |
| my-votes/[id]                  | GET         | Get my vote                                                      | User representing organization |
| my-votes/[id]                  | DELETE      | Take back my vote                                                | User representing organization |
| admin-users                    | GET         | Lists all users                                                  | Admin                          |
| admin-users                    | POST        | Add new user                                                     | Admin                          |
| admin-users/[id]               | GET         | Get user                                                         | Admin                          |
| admin-users/[id]               | PUT         | Updates user (including represented restaurant and/or org)       | Admin                          |
| admin-users/[id]               | DELETE      | Delete user                                                      | Admin                          |
| admin-restaurants              | GET         | Lists all restaurants                                            | Admin                          |
| admin-restaurants              | POST        | Add new restaurant                                               | Admin                          |
| admin-restaurants/[id]         | GET         | Get restaurant                                                   | Admin                          |
| admin-restaurants/[id]         | PUT         | Update restaurant                                                | Admin                          |
| admin-restaurants/[id]         | DELETE      | Delete restaurant                                                | Admin                          |
| admin-organizations            | GET         | Lists all organizations                                          | Admin                          |
| admin-organizations            | POST        | Add new organization                                             | Admin                          |
| admin-organizations/[id]       | GET         | Get organization                                                 | Admin                          |
| admin-organizations/[id]       | PUT         | Update organization                                              | Admin                          |
| admin-organizations/[id]       | DELETE      | Delete organization                                              | Admin                          |
| admin-menus                    | GET         | Lists all menus                                                  | Admin                          |
| admin-menus/[id]               | GET         | Get menu                                                         | Admin                          |
| admin-menus/[id]               | DELETE      | Delete menu                                                      | Admin                          |
| admin-votes                    | GET         | Lists all votes                                                  | Admin                          |

## Tools and best practices used

**Clean code**

- Python code is formatted with `black` and checked with `flake8`
- No `flake8` rules are ignored, except `max-line-length` is set higher than default
- Python code complexity limit is enforced with `flake8` setting `max-complexity`. Currently 5 (see `setup.cfg`).

**Automated tests**

- Functionality is tested with `pytest`
- Test coverage is measured with `pytest-cov`
- Test coverage is enforced with `pytest-cov` setting `fail_under`. Currently 80% (see `setup.cfg`).
- Complex queries are extensively tested with different scenarios the help of `pytest.mark.parametrize`

**Development setup (backend developer experience)**

- One-line command to install, launch services and run application locally with `make run`
- Isolated python environment with `virtualenv`
- Simple installation of database, file server and logging service with `docker-compose`
- Database, file server and logging service all have UI admin consoles running locally
- Automated service startup, checks, tests and migrations checkup are done automatically before any `make` command
- Ability to run app in demo mode with minimal dependencies and no additional services with `docker-compose`
- In-line debugging setup for application run and test run for VSC IDE
- Automated `black` formatting setup on file save for VSC IDE

**API user experience (frontend developer experience)**

- All resources are designed as lists, even when it will always contain no more than one item. This is to keep API consistent and predictable.
- Hyperlinked serialization and other features of `django-rest-framework` was used for API to be easily discoverable and manually testable even without frontend app

**Logging**

- Logs are aggregated to `Graylog`, which stores them in structured format and allows queries (has `ElasticSearch` and `MongoDB` behind it)
- All requests has additional info logged about logged in user in custom `Django middleware`. Can be extended with more info.
- Full audit of data changes in "historical data" tables with `django-simple-history` package

**File management**

- To not restrict app scalability and keep it stateless, files are managed in separate Amazon S3 compatible service `Minio`

## Development instructions

**Prerequisites:**

- Docker
- Docker compose
- Python3 (tested with 3.8.2, possibly works with older versions as well)
- Virtualenv
- Make

**To create superadmin user:**

1. `make createsuperuser`

**To start application locally:**

1. `make run`
2. Open http://localhost:8000

Clarification: `make run` (or any `make` command) will ensure a few things automatically, before starting the app:

1. Install dependencies (virtualenv, pip install)
2. Perform checks (formatting, linting)
3. Startup local DBs, file service, logging service
4. Apply migrations
5. Run tests

**To do some testing locally:**

1. Start and open http://localhost:8000
2. Create a few users while posting "registration form" to http://localhost:8000/api/v1/my-user/
3. Login as admin
4. Create a few restaurants while posting here: http://localhost:8000/api/v1/admin-restaurants/
5. Create a few orgs while posting here: http://localhost:8000/api/v1/admin-organizations/
6. Update a few users to let them represent a restaurant and/or org here: http://localhost:8000/api/v1/admin-users/
7. Logout
8. Login as one of restaurant representing users
9. Upload todays menu here: http://localhost:8000/api/v1/my-restaurant-todays-menu/
10. Do the steps 8&9 for other restaurant user
11. Login as org representing user
12. See my todays voting options and todays stats: http://localhost:8000/api/v1/my-todays-options/
13. Post vote: http://localhost:8000/api/v1/my-votes/
14. See updated stats http://localhost:8000/api/v1/my-todays-options/, notice which restaurant is marked as winner

**To start debugging:**

Configure and start debugging for your IDE. Details:

- Command before startup: `make`
- Startup command: `env/bin/python manage.py runserver`
- Example configuration for Visual Studio Code is here: `.vscode/launch.json`

**To run checks (linting, formatting) and tests:**

1. `make test`

**To check DB contents via pgadmin**

1. `make`
2. Open http://localhost:8001
3. Login with `admin:password` and connect to Main db (password: `postgres`)

**To check uploaded files via Minio browser**

1. `make`
2. Open http://localhost:8002
3. Login with `minio_admin:minio_password`

**To check logs in Graylog**

1. `make`
2. Open http://localhost:8003
3. Login with `admin:admin`
4. (First time only) configure new input (GELF UDP on port 12201) here: http://localhost:8003/system/inputs
5. See messages in "All messages" stream here: http://localhost:8003/streams
