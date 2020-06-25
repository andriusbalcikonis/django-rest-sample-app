import pytest
from datetime import datetime, timedelta
from menuratings.mr.models import User, Restaurant, Organization, Menu, Vote
from menuratings.mr.helpers.complex_queries import get_voting_results_of_the_day

# Unit tests of complex query "get_voting_results_of_the_day" logic

NUM_OF_DAYS = 7
NUM_OF_RESTAURANTS = 3
NUM_OF_USERS = 10

# Today will be Wednesday in these tests (see "generate_day" function)
TODAY_WEDNESDAY = 0
YESTERDAY_TUESDAY = 1
MONDAY = 2
SUNDAY = 3
SATURDAY = 4
FRIDAY = 5
THURSDAY = 6


tests = [
    {
        "scenario": "No votes - empty results",
        "input_votes": [],
        "expected_output_results": [],
    },
    {
        "scenario": "One vote yesterday - still empty results today",
        "input_votes": [{"day": YESTERDAY_TUESDAY, "user": 0, "menu": 0}],
        "expected_output_results": [],
    },
    {
        "scenario": "One vote today - OK, can be seen in results",
        "input_votes": [{"day": TODAY_WEDNESDAY, "user": 0, "menu": 0}],
        "expected_output_results": [{"menu": 0, "total_votes": 1, "winner": True}],
    },
    {
        "scenario": "One vote today, but by user from other org - empty results",
        "input_votes": [
            {"day": TODAY_WEDNESDAY, "other_org": True, "user": 0, "menu": 0}
        ],
        "expected_output_results": [],
    },
    {
        "scenario": "Menu '1' wins with 3 votes",
        "input_votes": [
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 1},
            {"day": TODAY_WEDNESDAY, "user": 2, "menu": 1},
            {"day": TODAY_WEDNESDAY, "user": 3, "menu": 1},
            {"day": TODAY_WEDNESDAY, "user": 4, "menu": 2},
            {"day": TODAY_WEDNESDAY, "user": 5, "menu": 2},
        ],
        "expected_output_results": [
            {"menu": 1, "total_votes": 3, "winner": True},
            {"menu": 2, "total_votes": 2},
            {"menu": 0, "total_votes": 1},
        ],
    },
    {
        "scenario": "Equal votes, menu '0' wins, because first vote was for it",
        "input_votes": [
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 1},
        ],
        "expected_output_results": [
            {"menu": 0, "total_votes": 1, "winner": True},
            {"menu": 1, "total_votes": 1},
        ],
    },
    {
        "scenario": "Equal votes, menu '1' wins, because first vote was for it",
        "input_votes": [
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 1},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 0},
        ],
        "expected_output_results": [
            {"menu": 1, "total_votes": 1, "winner": True},
            {"menu": 0, "total_votes": 1},
        ],
    },
    {
        "scenario": (
            "Menu '0' has most votes three workdays in a row, "
            "so third day menu '1' option is declared as winner"
        ),
        "input_votes": [
            {"day": MONDAY, "user": 0, "menu": 0},
            {"day": MONDAY, "user": 1, "menu": 0},
            {"day": YESTERDAY_TUESDAY, "user": 0, "menu": 0},
            {"day": YESTERDAY_TUESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 2, "menu": 1},
        ],
        "expected_output_results": [
            {"menu": 0, "total_votes": 2},
            {"menu": 1, "total_votes": 1, "winner": True},
        ],
    },
    {
        "scenario": (
            "Menu '0' has most votes four workdays in a row, ",
            "so yesterday it was skipped, today it can be the winner again",
        ),
        "input_votes": [
            {"day": FRIDAY, "user": 0, "menu": 0},
            {"day": FRIDAY, "user": 1, "menu": 0},
            {"day": MONDAY, "user": 0, "menu": 0},
            {"day": MONDAY, "user": 1, "menu": 0},
            {"day": YESTERDAY_TUESDAY, "user": 0, "menu": 0},
            {"day": YESTERDAY_TUESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 2, "menu": 1},
        ],
        "expected_output_results": [
            {"menu": 0, "total_votes": 2, "winner": True},
            {"menu": 1, "total_votes": 1},
        ],
    },
    {
        "scenario": (
            "Menu '0' has most votes four days in a row, ",
            "but if we count workdays - three, ",
            "so today it needs to be skipped",
        ),
        "input_votes": [
            {"day": SUNDAY, "user": 0, "menu": 0},
            {"day": SUNDAY, "user": 1, "menu": 0},
            {"day": MONDAY, "user": 0, "menu": 0},
            {"day": MONDAY, "user": 1, "menu": 0},
            {"day": YESTERDAY_TUESDAY, "user": 0, "menu": 0},
            {"day": YESTERDAY_TUESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 2, "menu": 1},
        ],
        "expected_output_results": [
            {"menu": 0, "total_votes": 2},
            {"menu": 1, "total_votes": 1, "winner": True},
        ],
    },
    {
        "scenario": (
            "On Monday there was a 3 workday streak for menu '1',",
            "so menu '0' was declared winner, ",
            "this means, that '0' has a streak today",
            "and cannot be declared winner today",
        ),
        "input_votes": [
            {"day": THURSDAY, "user": 0, "menu": 1},
            {"day": FRIDAY, "user": 0, "menu": 1},
            {"day": MONDAY, "user": 0, "menu": 0},
            {"day": MONDAY, "user": 1, "menu": 1},
            {"day": MONDAY, "user": 2, "menu": 1},
            {"day": YESTERDAY_TUESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 0, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 1, "menu": 0},
            {"day": TODAY_WEDNESDAY, "user": 2, "menu": 1},
        ],
        "expected_output_results": [
            {"menu": 0, "total_votes": 2},
            {"menu": 1, "total_votes": 1, "winner": True},
        ],
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
    current_day = days_and_menus[TODAY_WEDNESDAY]["day"]

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
        day = generate_day(day_index)

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
        menu = days_and_menus[TODAY_WEDNESDAY]["day_menus"][line["menu"]]
        transformed_line = {
            "menu__restaurant_id": menu.restaurant.id,
            "total_votes": line["total_votes"],
        }
        if line.get("winner"):
            transformed_line["winner"] = line.get("winner")
        transformed.append(transformed_line)
    return transformed


def generate_day(day_index):
    # Taking 2020-01-01 (it was wednesday) as TODAY_WEDNESDAY
    return datetime(2020, 1, 1) - timedelta(days=day_index)
