# Django REST Framework
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

# Third party
import pytest

# Own
from core.rest.v1.views import Ping


class TestPing:
    @pytest.mark.django_db
    def test_get_ping(self):
        Ping.throttle_classes = ()

        client = APIClient()
        response = client.get(reverse("v1:ping"), format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == "pong"

    @pytest.mark.django_db
    def test_post_ping(self):
        Ping.throttle_classes = ()

        client = APIClient()
        response = client.post(reverse("v1:ping"), format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == "pong"
