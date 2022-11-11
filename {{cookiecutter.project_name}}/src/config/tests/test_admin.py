# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status

# Third party
import pytest


class TestCustomAdminSite:
    @pytest.mark.django_db
    def test_index_applies_user_language(self, client, user_alice):
        # Test that nothing goes wrong when requested by an anonymous user
        response = client.get(reverse("admin:index"))
        assert "django_language" not in response.cookies.keys()

        # Test the actual feature when a user is logged in
        client.force_login(user_alice, "django.contrib.auth.backends.ModelBackend")
        response = client.get(reverse("admin:index"))
        assert response.cookies["django_language"].value == user_alice.language

    @pytest.mark.django_db
    def test_login_applies_user_language(self, client, user_alice):
        # Test that nothing goes wrong when requested by an anonymous user
        response = client.get(reverse("admin:login"))
        assert "django_language" not in response.cookies.keys()

        # Test the actual feature when a user is logging in
        response = client.post(reverse("admin:login"), {"username": user_alice.username, "password": "abc123"})
        assert response.cookies["django_language"].value == user_alice.language


class TestSimplerAutocomplete:
    def setup_method(self):
        self.url = reverse("admin:simpler_autocomplete")

    @pytest.mark.django_db
    def test_successful_requests(self, client, user_superuser, user_alice, user_bob):
        client.force_login(user_superuser, "django.contrib.auth.backends.ModelBackend")
        # With "username" field as value field
        response = client.get(self.url, {"app_label": "users", "model_name": "user", "value_field": "username"})
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        # 3 users: user_superuser, user_alice, user_bob
        assert len(response_json["results"]) == 3
        sorted_results = sorted(response_json["results"], key=lambda result: result["id"])
        assert sorted_results[0]["id"] == user_alice.username
        assert sorted_results[1]["id"] == user_bob.username
        assert sorted_results[2]["id"] == user_superuser.username

        # With "pk" field as value field
        response = client.get(self.url, {"app_label": "users", "model_name": "user", "value_field": "pk"})
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        # 3 users: user_superuser, user_alice, user_bob
        assert len(response_json["results"]) == 3
        sorted_results = sorted(response_json["results"], key=lambda result: result["id"])
        assert sorted_results[0]["id"] == sorted_results[0]["pk"] == str(user_superuser.pk)
        assert sorted_results[1]["id"] == sorted_results[1]["pk"] == str(user_alice.pk)
        assert sorted_results[2]["id"] == sorted_results[2]["pk"] == str(user_bob.pk)

    def test_missing_get_param(self, client, user_superuser):
        client.force_login(user_superuser, "django.contrib.auth.backends.ModelBackend")

        # Missing app_label
        response = client.get(self.url, {"model_name": "user", "value_field": "username"})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        # Missing model_name
        response = client.get(self.url, {"app_label": "users", "value_field": "username"})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        # Missing value_field
        response = client.get(self.url, {"app_label": "users", "model_name": "user"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_model(self, client, user_superuser):
        client.force_login(user_superuser, "django.contrib.auth.backends.ModelBackend")
        response = client.get(self.url, {"app_label": "users", "model_name": "foo", "value_field": "username"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_list_model_objects(self, client, user_alice):
        # Remove user from all groups to remove permission to view users
        user_alice.groups.clear()
        client.force_login(user_alice, "django.contrib.auth.backends.ModelBackend")

        assert not user_alice.has_perm("users.view_user")
        response = client.get(self.url, {"app_label": "users", "model_name": "user", "value_field": "username"})
        assert response.status_code == status.HTTP_403_FORBIDDEN
