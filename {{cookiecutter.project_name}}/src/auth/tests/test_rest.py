# Django
from django.contrib.auth.hashers import make_password
from django.urls import reverse

# Third party
import pytest

# Own
from auth.rest import UserTokenAuthentication


class TestUserTokenAuthentication:
    def setup_method(self):
        self.backend = UserTokenAuthentication()
        self.url_ping = reverse("core.rest:ping")

    @pytest.mark.django_db
    def test_authenticate_success(self, settings, rf, user_alice):
        raw_access_token = "def456"
        user_alice.access_token = make_password(raw_access_token, settings.SECRET_KEY)
        user_alice.save()
        request = rf.get(self.url_ping, HTTP_AUTHORIZATION=f"Bearer {raw_access_token}")
        user, token = self.backend.authenticate(request)
        assert user == user_alice
        assert token is None

    @pytest.mark.django_db
    def test_authenticate_failure(self, settings, rf, user_alice):
        raw_access_token = "def456"
        user_alice.access_token = make_password(raw_access_token, settings.SECRET_KEY)
        user_alice.save()
        request = rf.get(self.url_ping, HTTP_AUTHORIZATION="Bearer ghi678")
        response = self.backend.authenticate(request)
        assert response is None

    def test_authenticate_missing_authorization_header(self, rf):
        request = rf.get(self.url_ping)
        response = self.backend.authenticate(request)
        assert response is None
