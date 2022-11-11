# Django
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Django REST Framework
from rest_framework import status

# Third party
import pytest
from axes.models import AccessAttempt

# Own
from ..views import CustomPasswordResetConfirmView


class TestPasswordResetConfirmView:
    @pytest.mark.django_db
    def test_axes_reset(self, rf, client, user_alice):
        # Fail login twice
        client.post(reverse("admin:login"), {"username": user_alice.username, "password": "wrong_password"})
        client.post(reverse("admin:login"), {"username": user_alice.username, "password": "wrong_password"})

        # Check that Axes noticed
        attempts = AccessAttempt.objects.get(username=user_alice.username)
        assert attempts.failures_since_start == 2

        # Use password reset form to reset Axes access attempts
        url_uidb64 = urlsafe_base64_encode(force_bytes(user_alice.pk))
        url_token = CustomPasswordResetConfirmView.reset_url_token
        url = reverse("password_reset_confirm", kwargs={"uidb64": url_uidb64, "token": url_token})
        session_token = PasswordResetTokenGenerator().make_token(user_alice)
        form_data = {
            "new_password1": "def456",
            "new_password2": "def456",
        }
        form = SetPasswordForm(user_alice, data=form_data)
        form.full_clean()
        request = rf.post(url, form_data)
        request.session = {INTERNAL_RESET_SESSION_TOKEN: session_token}
        CustomPasswordResetConfirmView(request=request).form_valid(form)

        # Check that Axes access attempts were successfully reset
        attempts = AccessAttempt.objects.filter(username=user_alice.username)
        assert len(attempts) == 0


class TestSignalAxesBanJWTLoginRoute:
    def test_ban(self, settings, client, user_alice):
        url = reverse("token_obtain_pair")
        payload = {"username": user_alice.username, "password": "wrong_password"}

        access_attemps = AccessAttempt.objects.filter(username=user_alice.username)
        assert len(access_attemps) == 0

        for __ in range(settings.AXES_FAILURE_LIMIT - 1):
            response = client.post(url, payload)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.post(url, payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["code"] == "AXES_BAN"

        # Sanity check: a request to another non-protected route should be OK
        response = client.get(reverse("core:index"))
        assert response.status_code == status.HTTP_200_OK
