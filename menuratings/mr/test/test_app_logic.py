from django.urls import reverse
from rest_framework import status
from menuratings.mr.models import User


# Constants:

ADMIN_USER_USERNAME = "admin"
ANY_USER_PWD = "admin"
ANY_USER_EMAIL = "some@email.com"


# Tests. User list - functional tests.


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
    url = select_first_item(user_list)["url"]
    user = http_get_user(client, url)

    # Check it's name:
    assert select_field(user, "username") == username


def test_normal_user_can_edit_his_data(client, db):
    username = "some_new_user"
    first_name = "First name"
    last_name = "Last name"

    do_create_user_and_login(client, username)

    # Get userlist:
    user_list = http_get_user_list(client)

    # Update user item:
    user_item = select_first_item(user_list)
    user_item["first_name"] = first_name
    user_item["last_name"] = last_name
    user = http_put_user(client, user_item)
    assert user.status_code == status.HTTP_200_OK

    # Get user item:
    url = select_field(user, "url")
    user = http_get_user(client, url)

    # Check it's username and names:
    assert select_field(user, "username") == username
    assert select_field(user, "first_name") == first_name
    assert select_field(user, "last_name") == last_name


# Helpers. Reused test blocks:


def do_login(client, username):
    client.login(username=username, password=ANY_USER_PWD)


def do_create_user_and_login(client, username):
    created_user = http_post_user(client, username)
    assert created_user.status_code == status.HTTP_201_CREATED
    do_login(client, username)


# Helpers. Initial conditions:


def set_initial_conditions_only_admin_user():
    User.objects.create_superuser(ADMIN_USER_USERNAME, "admin@admin.com", ANY_USER_PWD)


# Helpers. Requests:


def http_get_user_list(client):
    return client.get(reverse("user-list"))


def http_post_user(client, username):
    return client.post(
        reverse("user-list"),
        data={"username": username, "email": ANY_USER_EMAIL, "password": ANY_USER_PWD},
    )


def http_get_user(client, url):
    return client.get(url)


def http_put_user(client, user_item):
    return client.put(user_item["url"], data=user_item)


# Helpers. Assertions


def assert_result_count(response, count):
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == count


# Helpers. Selectors:


def select_first_item(response):
    return response.data["results"][0]


def select_field(response, field_name):
    return response.data[field_name]
