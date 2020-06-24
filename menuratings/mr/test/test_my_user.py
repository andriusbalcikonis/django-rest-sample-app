from django.urls import reverse
from rest_framework import status
from menuratings.mr.test.helpers import (
    assert_result_count,
    do_create_user_and_login,
    select_first_item,
    select_field,
    set_initial_conditions_only_admin_user,
)

# FUNCTIONAL TESTS


def test_user_list_for_anonymous_user_is_accessible_but_empty(client, db):
    user_list = http_get_myuser_list(client)
    assert_result_count(user_list, 0)


def test_user_list_for_anonymous_user_is_accessible_but_empty_even_if_users_exist_in_db(
    client, db
):
    set_initial_conditions_only_admin_user()
    user_list = http_get_myuser_list(client)
    assert_result_count(user_list, 0)


def test_user_list_for_anonymous_user_allows_to_create_new_user(client, db):
    username = "some_new_user"
    do_create_user_and_login(client, username)


def test_normal_user_can_view_his_data(client, db):
    username = "some_new_user"

    do_create_user_and_login(client, username)

    # Get userlist:
    user_list = http_get_myuser_list(client)

    # Get user item:
    url = select_first_item(user_list)["url"]
    user = http_get_myuser(client, url)

    # Check it's name:
    assert select_field(user, "username") == username


def test_normal_user_can_edit_his_data(client, db):
    username = "some_new_user"
    first_name = "First name"
    last_name = "Last name"

    do_create_user_and_login(client, username)

    # Get userlist:
    user_list = http_get_myuser_list(client)

    # Update user item:
    user_item = select_first_item(user_list)
    user_item["first_name"] = first_name
    user_item["last_name"] = last_name
    user_item["represented_restaurant"] = ""
    user_item["represented_organization"] = ""
    user = http_put_myuser(client, user_item)
    assert user.status_code == status.HTTP_200_OK

    # Get user item:
    url = select_field(user, "url")
    user = http_get_myuser(client, url)

    # Check it's username and names:
    assert select_field(user, "username") == username
    assert select_field(user, "first_name") == first_name
    assert select_field(user, "last_name") == last_name


# Helpers - HTTP requests:


def http_get_myuser_list(client):
    return client.get(reverse("my-user-list"))


def http_get_myuser(client, url):
    return client.get(url)


def http_put_myuser(client, user_item):
    return client.put(user_item["url"], data=user_item)
