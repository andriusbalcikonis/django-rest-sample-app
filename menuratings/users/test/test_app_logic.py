import pytest
from menuratings.menuratings.models import Restaurant


@pytest.mark.django_db
def test_smth():

    r = Restaurant(name="From tests")
    r.save()

    r = Restaurant(name="From tests 2")
    r.save()

    all = Restaurant.objects.all()

    assert len(all) == 2
