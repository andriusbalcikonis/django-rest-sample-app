from django.urls import reverse
from rest_framework import status
from menuratings.mr.models import User


# Constants:

ADMIN_USER_USERNAME = "admin"
ADMIN_USER_PWD = "admin"


# Tests. User list


def test_user_list_for_anonymous_user_is_accessible_but_empty(client, db):
    set_initial_conditions_empty_db()
    response = http_get_user_list(client)
    assert_result_count(response, 0)


def test_user_list_for_admin_user_is_accessible_and_has_one_item(client, db):
    set_initial_conditions_only_admin_user()
    login_as_admin(client)
    response = http_get_user_list(client)
    assert_result_count(response, 1)


# Helpers. Initial conditions:


def set_initial_conditions_empty_db():
    pass


def set_initial_conditions_only_admin_user():
    User.objects.create_superuser(
        ADMIN_USER_USERNAME, "admin@admin.com", ADMIN_USER_PWD
    )


# Helpers. Login:


def login_as_admin(client):
    client.login(username=ADMIN_USER_USERNAME, password=ADMIN_USER_PWD)


# Helpers. Requests:


def http_get_user_list(client):
    return client.get(reverse("user-list"))


# Helpers. Assertions


def assert_result_count(response, count):
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == count
