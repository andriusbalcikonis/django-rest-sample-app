from datetime import timedelta
from itertools import groupby
from django.db.models import Count
from menuratings.mr.models import Vote


# Complex queries


def get_voting_results_of_the_day(date, organization_id):
    """
    This is a tricky one.
    Theoretically, there may be cases, when we need full history to declare todays winner.
    So this algorithm always collects full voting hisory for this org and calculates precisely.
    This is due to the rule "there may not be same winner for three consequitive working days"
    """

    voting_stats_history = _get_full_voting_stats_for_org(organization_id)
    voting_stats_history_by_day = _group_voting_stats_by_day(voting_stats_history)

    todays_stats = voting_stats_history_by_day.get(_get_date_key(date))

    if todays_stats:

        if not _date_is_workday(date):
            # If today is not a workday, everything is simple.
            # Just delcare the restaurant with most votes (first in sorted list) as winner
            top_item = todays_stats[0]
            _mark_as_winner(top_item)

        else:

            # Use recursive algorithm to check
            # rule "there may not be same winner for three consequitive working days"

            winners_cache = {}
            winner_restaurant_id = _get_winner_of_workday_recursively(
                voting_stats_history_by_day, winners_cache, date
            )

            for item in todays_stats:
                if item["menu__restaurant_id"] == winner_restaurant_id:
                    _mark_as_winner(item)

    else:
        todays_stats = []

    return todays_stats


# Helpers


def _get_full_voting_stats_for_org(organization_id):

    # Take all votes
    query = Vote.objects

    # Filter only the votes posted by users of current org:
    query = query.filter(voter__represented_organization_id=organization_id)

    # Group votes by restaurant and date, calculate vote count for each group:
    query = (
        query.values("menu__date", "menu__restaurant_id")
        .annotate(total_votes=Count("menu__restaurant_id"))
        .order_by("menu__date")
    )

    # Run the query
    results = list(query)

    return results


def _group_voting_stats_by_day(voting_stats_hisory):
    def take_menu_date(item):
        return item["menu__date"]

    grouped = {}
    for date, group in groupby(voting_stats_hisory, take_menu_date):

        days_stats = [
            {
                "menu__restaurant_id": x["menu__restaurant_id"],
                "total_votes": x["total_votes"],
            }
            for x in group
        ]

        days_stats = _sort_days_stats(days_stats)
        grouped[_get_date_key(date)] = days_stats

    return grouped


def _sort_days_stats(days_stats):
    def take_total_votes(item):
        return item["total_votes"]

    return sorted(days_stats, reverse=True, key=take_total_votes)


def _date_is_workday(date):
    """
    Trivial checking of id day is workday.
    To check properly, it should be some calendar API of holidays called,
    but this is out of scope of this project.
    """
    weekday = date.weekday()
    SATURDAY = 5
    SUNDAY = 6
    return weekday not in [SATURDAY, SUNDAY]


def _mark_as_winner(item):
    item["winner"] = True


def _get_date_key(date):
    # Making sure date key is consistently generated:
    return "{}-{}-{}".format(date.year, date.month, date.day)


def _get_previous_workday(date):
    potential_workday = date - timedelta(days=1)
    while not _date_is_workday(potential_workday):
        potential_workday = potential_workday - timedelta(days=1)
    return potential_workday


def _get_winner_of_workday_recursively(
    voting_stats_history_by_day, winners_cache, date
):
    """
    Recursive function to check the winner, while following
    the rule "there may not be same winner for three consequitive working days"
    """

    today = date
    todays_key = _get_date_key(today)
    todays_stats = voting_stats_history_by_day.get(todays_key)

    # First quick check - if no stats for today, no winner for to day:
    if not todays_stats:
        winners_cache[todays_key] = None
        return None

    # Second quick check - cache is used to not explode in run time of this recursiveness:
    if todays_key in winners_cache.keys():
        return winners_cache[todays_key]

    # Else we need to get back into history and make sure there is no winner streaks:
    first_place_today = (
        todays_stats[0]["menu__restaurant_id"] if len(todays_stats) > 0 else None
    )
    second_place_today = (
        todays_stats[1]["menu__restaurant_id"] if len(todays_stats) > 1 else None
    )

    workday_before = _get_previous_workday(today)
    workday_before_winner = _get_winner_of_workday_recursively(
        voting_stats_history_by_day, workday_before
    )

    if first_place_today != workday_before_winner:
        # Great, even previous day did not match, so no need to check further,
        # first place is ok as a winner:
        return first_place_today
    else:
        # Need to check two workdays before:
        workday_before2 = _get_previous_workday(workday_before)
        workday_before2_winner = _get_winner_of_workday_recursively(
            voting_stats_history_by_day, workday_before2
        )

        # Check the winner to avoid three workday streak:
        winner = (
            first_place_today
            if first_place_today != workday_before2_winner
            else second_place_today
        )
        winners_cache[todays_key] = winner
        return winner
