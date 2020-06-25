# Django REST sample app

## Intro

This is a simple django rest app, which I built as an excersize.

## Requirements

TODO

## Solution - Functionality design

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

## Solution - API design

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

**To check uploaded files via Minio browser**

1. `make`
2. Open http://localhost:8002
3. Login with `minio_admin:minio_password`

**To start debugging:**

Configure and start debugging for your IDE. Details:

- Command before startup: `make`
- Startup command: `env/bin/python manage.py runserver`
- Example configuration for Visual Studio Code is here: `.vscode/launch.json`
