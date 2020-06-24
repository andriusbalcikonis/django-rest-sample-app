from django.db.models import Count
from menuratings.mr.models import Vote


def get_voting_results_of_the_day(date, organization_id):

    # Take all votes
    query = Vote.objects

    # Filter only of todays:
    query = query.filter(menu__date=date)

    # Filter only the votes posted by users of current org:
    query = query.filter(voter__represented_organization_id=organization_id)

    # Group votes by menu, take vote count and order by it:
    query = (
        query.values("menu_id")
        .annotate(total_votes=Count("menu"))
        .order_by("-total_votes")
    )

    # Run the query
    results = list(query)

    return results
