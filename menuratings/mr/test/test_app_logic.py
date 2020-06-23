from django.urls import reverse
from rest_framework import status
from menuratings.mr.models import User


# Constants:

ADMIN_USER_USERNAME = "admin"
ANY_USER_PWD = "admin"
ANY_USER_EMAIL = "some@email.com"


# Tests. User list


def test_user_list_for_anonymous_user_is_accessible_but_empty(client, db):
    response = http_get_user_list(client)
    assert_result_count(response, 0)


def test_user_list_for_anonymous_user_is_accessible_but_empty_even_if_users_exist_in_db(
    client, db
):
    set_initial_conditions_only_admin_user()
    response = http_get_user_list(client)
    assert_result_count(response, 0)


def test_user_list_for_admin_user_is_accessible_and_has_one_item(client, db):
    set_initial_conditions_only_admin_user()
    login(client, ADMIN_USER_USERNAME)

    response = http_get_user_list(client)
    assert_result_count(response, 1)


def test_user_list_for_anonymous_user_allows_to_create_user_and_new_user_is_able_to_login(
    client, db
):
    username = "some_new_user"

    # Create:
    response = http_post_create_user_form(client, username)
    assert_created_successfully(response)

    # Try to login:
    login(client, username)

    # Userlist contains single item:
    response = http_get_user_list(client)
    assert_result_count(response, 1)


# Helpers. Initial conditions:


def set_initial_conditions_only_admin_user():
    User.objects.create_superuser(ADMIN_USER_USERNAME, "admin@admin.com", ANY_USER_PWD)


# Helpers. Login:


def login(client, username):
    client.login(username=username, password=ANY_USER_PWD)


# Helpers. Requests:


def http_get_user_list(client):
    return client.get(reverse("user-list"))


def http_post_create_user_form(client, username):
    return client.post(
        reverse("user-list"),
        data={"username": username, "email": ANY_USER_EMAIL, "password": ANY_USER_PWD},
    )


# Helpers. Assertions


def assert_result_count(response, count):
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == count


def assert_created_successfully(response):
    assert response.status_code == status.HTTP_201_CREATED
