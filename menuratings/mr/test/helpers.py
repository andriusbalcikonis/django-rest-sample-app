from django.urls import reverse
from rest_framework import status
from menuratings.mr.models import User

# Constants:

ADMIN_USER_USERNAME = "admin"
ANY_USER_PWD = "admin"
ANY_USER_EMAIL = "some@email.com"

# Reused test blocks:


def do_login(client, username):
    client.login(username=username, password=ANY_USER_PWD)


def do_create_user_and_login(client, username):
    created_user = client.post(
        reverse("my-user-list"),
        data={"username": username, "email": ANY_USER_EMAIL, "password": ANY_USER_PWD},
    )
    assert created_user.status_code == status.HTTP_201_CREATED
    do_login(client, username)


# Initial conditions:


def set_initial_conditions_only_admin_user():
    User.objects.create_superuser(ADMIN_USER_USERNAME, "admin@admin.com", ANY_USER_PWD)


# Assertions


def assert_result_count(response, count):
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == count


# Selectors:


def select_first_item(response):
    return response.data["results"][0]


def select_field(response, field_name):
    return response.data[field_name]
