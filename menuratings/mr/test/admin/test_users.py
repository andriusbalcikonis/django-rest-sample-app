from django.urls import reverse
from menuratings.mr.test.helpers import (
    ADMIN_USER_USERNAME,
    assert_result_count,
    do_login,
    set_initial_conditions_only_admin_user,
)


# FUNCTIONAL TESTS


def test_user_list_for_admin_user_is_accessible_and_has_one_item(client, db):
    set_initial_conditions_only_admin_user()
    do_login(client, ADMIN_USER_USERNAME)

    user_list = http_get_user_list(client)
    assert_result_count(user_list, 1)


# Helpers. Requests:


def http_get_user_list(client):
    return client.get(reverse("user-list"))
