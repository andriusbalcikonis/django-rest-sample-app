import pytest
from menuratings.mr.models import User

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_list(client):

    password = "admin"
    admin = User.objects.create_superuser("admin", "admin@admin.com", password)
    client.login(username=admin.username, password=password)

    response = client.get(reverse("user-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
