# Django REST sample app

## Intro

This is a simple django rest app, which I built as a job-interview task.

## Requirements

TODO

## Solution - API design

| Endpoint                       | HTTP method | Action                                                            | Allowed for users              |
| :----------------------------- | :---------- | :---------------------------------------------------------------- | :----------------------------- |
| my-user                        | POST        | Create new user                                                   | Anonymous                      |
| my-user                        | GET         | Get my user profile (including represented restaurant and/or org) | Any user                       |
| my-user                        | PUT         | Update my user profile details                                    | Any user                       |
| my-user                        | DELETE      | Delete my user                                                    | Any user                       |
| my-restaurant-users            | GET         | Lists users of my restaurant                                      | User representing restaurant   |
| my-restaurant-users            | POST        | Invites another user to my restaurant                             | User representing restaurant   |
| my-restaurant-users/[id]       | GET         | Lists users of my restaurant                                      | User representing restaurant   |
| my-restaurant-users/[id]       | DELETE      | Removes user from my restaurant                                   | User representing restaurant   |
| my-restaurant-todays-menu      | GET         | Get todays menu                                                   | User representing restaurant   |
| my-restaurant-todays-menu      | POST        | Create todays menu                                                | User representing restaurant   |
| my-restaurant-todays-menu      | PUT         | Update todays menu                                                | User representing restaurant   |
| my-restaurant-todays-menu      | DELETE      | Delete todays menu                                                | User representing restaurant   |
| my-organization-users          | GET         | Lists users of my organization                                    | User representing organization |
| my-organization-users          | POST        | Invites another user to my organization                           | User representing organization |
| my-organization-users/[id]     | GET         | Lists users of my organization                                    | User representing organization |
| my-organization-users/[id]     | DELETE      | Removes user from my organization                                 | User representing organization |
| my-organization-voting-results | GET         | Voting results inside my organization                             | User representing organization |
| my-todays-vote-options         | GET         | Lists todays vote options                                         | User representing organization |
| my-todays-vote                 | POST        | Post my vote                                                      | User representing organization |
| my-todays-vote                 | GET         | Get my vote                                                       | User representing organization |
| my-todays-vote                 | DELETE      | Take back my vote                                                 | User representing organization |
| admin-users                    | GET         | Lists all users                                                   | Admin                          |
| admin-users                    | POST        | Add new user                                                      | Admin                          |
| admin-users/[id]               | GET         | Get user                                                          | Admin                          |
| admin-users/[id]               | PUT         | Updates user (including represented restaurant and/or org)        | Admin                          |
| admin-users/[id]               | DELETE      | Delete user                                                       | Admin                          |
| admin-restaurants              | GET         | Lists all restaurants                                             | Admin                          |
| admin-restaurants              | POST        | Add new restaurant                                                | Admin                          |
| admin-restaurants/[id]         | GET         | Get restaurant                                                    | Admin                          |
| admin-restaurants/[id]         | PUT         | Update restaurant                                                 | Admin                          |
| admin-restaurants/[id]         | DELETE      | Delete restaurant                                                 | Admin                          |
| admin-organizations            | GET         | Lists all organizations                                           | Admin                          |
| admin-organizations            | POST        | Add new organization                                              | Admin                          |
| admin-organizations/[id]       | GET         | Get organization                                                  | Admin                          |
| admin-organizations/[id]       | PUT         | Update organization                                               | Admin                          |
| admin-organizations/[id]       | DELETE      | Delete organization                                               | Admin                          |
| admin-menus                    | GET         | Lists all menus                                                   | Admin                          |
| admin-menus/[id]               | GET         | Get menu                                                          | Admin                          |
| admin-menus/[id]               | DELETE      | Delete menu                                                       | Admin                          |
| admin-votes                    | GET         | Lists all votes                                                   | Admin                          |

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
