import pytest
from datetime import datetime
from menuratings.mr.models import User, Restaurant, Organization, Menu, Vote
from menuratings.mr.helpers.complex_queries import get_voting_results_of_the_day

# Unit tests of complex query "get_voting_results_of_the_day" logic

NUM_OF_DAYS = 5
NUM_OF_RESTAURANTS = 3
NUM_OF_USERS = 3

CURRENT_DAY_INDEX = NUM_OF_DAYS - 1


tests = [
    {
        "scenario": "No votes - empty results",
        "input_votes": [],
        "expected_output_results": [],
    },
    {
        "scenario": "One vote yesterday - still empty results today",
        "input_votes": [{"day": 3, "user": 0, "menu": 0}],
        "expected_output_results": [],
    },
    {
        "scenario": "One vote today - OK, can be seen in results",
        "input_votes": [{"day": 4, "user": 0, "menu": 0}],
        "expected_output_results": [{"menu": 0, "total_votes": 1}],
    },
    {
        "scenario": "One vote today, but by user from other org - empty results",
        "input_votes": [{"day": 4, "other_org": True, "user": 0, "menu": 0}],
        "expected_output_results": [],
    },
]


@pytest.mark.parametrize("test_data", tests)
def test_get_voting_results_of_the_day(test_data, db):

    input_votes = test_data["input_votes"]
    expected_output_results = test_data["expected_output_results"]

    # Step1. Preparation of data:
    restaurants = prepare_restaurants()
    days_and_menus = prepare_days_and_menus(restaurants)
    org, other_org = prepare_orgs()
    users, other_org_users = prepare_users(org, other_org)

    # Step2. Do voting:

    for vote_info in input_votes:
        menu = days_and_menus[vote_info["day"]]["day_menus"][vote_info["menu"]]
        user_list = other_org_users if vote_info.get("other_org") else users
        voter = user_list[vote_info["user"]]
        vote = Vote(voter=voter, menu=menu)
        vote.save()

    # Step 3. Pick current day:
    current_day = days_and_menus[CURRENT_DAY_INDEX]["day"]

    # Step 4. Execute the target function:
    results = get_voting_results_of_the_day(current_day, org.id)

    # Step 5. Transform expected output to have menu_ids:

    expected_output_results_transformed = transform_expected_output_results(
        expected_output_results, days_and_menus
    )

    # Step 6. Assert:
    assert results == expected_output_results_transformed


# Helpers - data preparation


def prepare_restaurants():
    restaurants = []
    for restaurant_index in range(NUM_OF_RESTAURANTS):
        restaurant = Restaurant(name="R{}".format(restaurant_index))
        restaurant.save()
        restaurants.append(restaurant)
    return restaurants


def prepare_days_and_menus(restaurants):
    days_and_menus = []
    for day_index in range(NUM_OF_DAYS):
        day = datetime(2020, 1, 1 + day_index)

        day_menus = []
        for restaurant_index in range(NUM_OF_RESTAURANTS):
            restaurant = restaurants[restaurant_index]
            days_menu = Menu(restaurant=restaurant, date=day)
            days_menu.save()

            day_menus.append(days_menu)

        days_and_menus.append({"day": day, "day_menus": day_menus})
    return days_and_menus


def prepare_orgs():
    org = Organization(name="Org")
    org.save()
    other_org = Organization(name="Other Org")
    other_org.save()
    return (org, other_org)


def prepare_users(org, other_org):
    users = []
    other_org_users = []
    for user_index in range(NUM_OF_USERS):
        user = User(username="user{}".format(user_index), represented_organization=org)
        user.save()
        users.append(user)
        other_org_user = User(
            username="other_org_user{}".format(user_index),
            represented_organization=other_org,
        )
        other_org_user.save()
        other_org_users.append(other_org_user)
    return (users, other_org_users)


def transform_expected_output_results(expected_output_results, days_and_menus):
    transformed = []
    for line in expected_output_results:
        menu = days_and_menus[CURRENT_DAY_INDEX]["day_menus"][line["menu"]]
        transformed_line = {"menu_id": menu.id, "total_votes": line["total_votes"]}
        transformed.append(transformed_line)
    return transformed
