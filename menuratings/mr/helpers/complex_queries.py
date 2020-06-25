from itertools import groupby
from django.db.models import Count
from menuratings.mr.models import Vote


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

        todays_stats = _sort_days_stats(todays_stats)

        if not _date_is_workday(date):

            # If today is not a workday, everything is simple.
            # Just delcare the restaurant with most votes (first in sorted list) as winner

            top_item = todays_stats[0]
            _mark_as_winner(top_item)

        else:

            pass

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

        group_items_cleaned_up = [
            {
                "menu__restaurant_id": x["menu__restaurant_id"],
                "total_votes": x["total_votes"],
            }
            for x in group
        ]

        grouped[_get_date_key(date)] = group_items_cleaned_up

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
