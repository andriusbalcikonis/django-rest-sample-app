import pytest
from menuratings.menuratings.models import Restaurant

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_smth():

    r = Restaurant(name="From tests")
    r.save()

    r = Restaurant(name="From tests 2")
    r.save()

    all = Restaurant.objects.all()

    assert len(all) == 2


@pytest.mark.django_db
def test_user_list(client):
    url = reverse("user-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 0
