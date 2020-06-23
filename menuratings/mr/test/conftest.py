import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """
    Use https://www.django-rest-framework.org/api-guide/testing/#apiclient
    To simplify work with PUT requests (https://www.django-rest-framework.org/api-guide/testing/#put-and-patch-with-form-data)  # noqa
    """
    return APIClient()
