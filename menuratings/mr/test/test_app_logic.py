from django.urls import reverse
from rest_framework import status
from menuratings.mr.models import User


# Constants:

ADMIN_USER_USERNAME = "admin"
ANY_USER_PWD = "admin"
ANY_USER_EMAIL = "some@email.com"


# Tests. User list


def test_user_list_for_anonymous_user_is_accessible_but_empty(client, db):
    user_list = http_get_user_list(client)
    assert_result_count(user_list, 0)


def test_user_list_for_anonymous_user_is_accessible_but_empty_even_if_users_exist_in_db(
    client, db
):
    set_initial_conditions_only_admin_user()
    user_list = http_get_user_list(client)
    assert_result_count(user_list, 0)


def test_user_list_for_admin_user_is_accessible_and_has_one_item(client, db):
    set_initial_conditions_only_admin_user()
    do_login(client, ADMIN_USER_USERNAME)

    user_list = http_get_user_list(client)
    assert_result_count(user_list, 1)


def test_user_list_for_anonymous_user_allows_to_create_new_user(client, db):
    username = "some_new_user"
    do_create_user_and_login(client, username)


def test_normal_user_can_view_his_data(client, db):
    username = "some_new_user"

    do_create_user_and_login(client, username)

    # Get userlist:
    user_list = http_get_user_list(client)

    # Get user item:
    url = select_first_item_field(user_list, "url")
    user_item = http_get_by_url(client, url)
    print(user_item)

    # Check it's name:
    created_username = select_field(user_item, "username")
    assert created_username == username


# Helpers. Reused test blocks:


def do_login(client, username):
    client.login(username=username, password=ANY_USER_PWD)


def do_create_user_and_login(client, username):
    created_user = http_post_create_user_form(client, username)
    assert_created_successfully(created_user)
    do_login(client, username)


# Helpers. Initial conditions:


def set_initial_conditions_only_admin_user():
    User.objects.create_superuser(ADMIN_USER_USERNAME, "admin@admin.com", ANY_USER_PWD)


# Helpers. Requests:


def http_get_by_url(client, url):
    return client.get(url)


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


# Helpers. Selectors:


def select_first_item_field(response, field_name):
    return response.data["results"][0][field_name]


def select_field(response, field_name):
    return response.data[field_name]
