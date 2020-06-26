from django.urls import reverse
from menuratings.mr.test.helpers import (
    assert_not_accessible,
    do_create_user_and_login,
    set_initial_conditions_one_restaurant_and_its_user,
    do_login,
    assert_created_ok,
    assert_result_count,
)

# FUNCTIONAL TESTS


def test_menu_list_for_anonymous_user_is_not_accessible(client, db):
    menu_list = http_get_my_restaurant_menu_list(client)
    assert_not_accessible(menu_list)


def test_menu_list_for_normal_user_is_not_accessible(client, db):
    username = "some_new_user"
    do_create_user_and_login(client, username)
    menu_list = http_get_my_restaurant_menu_list(client)
    assert_not_accessible(menu_list)


def test_menu_list_for_restaurant_user_is_accessible_but_empty(client, db):
    restaurant_name = "some_restaurant"
    username = "restaurant_user"
    set_initial_conditions_one_restaurant_and_its_user(
        client, restaurant_name, username
    )
    do_login(client, username)
    menu_list = http_get_my_restaurant_menu_list(client)
    assert_result_count(menu_list, 0)


def test_menu_list_for_restaurant_user_allows_to_post_todays_menu_but_only_one_time(
    client, db
):
    restaurant_name = "some_restaurant"
    username = "restaurant_user"
    set_initial_conditions_one_restaurant_and_its_user(
        client, restaurant_name, username
    )
    do_login(client, username)

    menu = {"contents": "some menu"}
    menu_list = http_post_my_restaurant_menu(client, menu)
    assert_created_ok(menu_list)

    menu = {"contents": "some other menu"}
    menu_list = http_post_my_restaurant_menu(client, menu)
    assert_not_accessible(menu_list)


# Helpers - HTTP requests:


def http_get_my_restaurant_menu_list(client):
    return client.get(reverse("my-restaurant-todays-menu-list"))


def http_get_my_restaurant_menu(client, url):
    return client.get(url)


def http_put_my_restaurant_menu(client, menu_item):
    return client.put(menu_item["url"], data=menu_item)


def http_post_my_restaurant_menu(client, menu_item):
    return client.post(reverse("my-restaurant-todays-menu-list"), data=menu_item)
