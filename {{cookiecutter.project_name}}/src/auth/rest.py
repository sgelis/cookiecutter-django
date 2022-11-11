# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# Django REST Framework
from rest_framework import authentication

User = get_user_model()


class UserTokenAuthentication(authentication.BaseAuthentication):
    """Authenticates incoming requests by matching `Authorization` header with user's `access_token`."""

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None
        token = token.split("Bearer")[-1].strip()
        hashed_token = make_password(token, settings.SECRET_KEY)

        try:
            user = User.objects.get(access_token=hashed_token)
        except User.DoesNotExist:
            # Do not raise `AuthenticationFailed` here, since downstream authentication classes might use the same
            # header (`Authorization`) to authenticated request (e.g.: `JWTAuthentication`).
            return None

        return user, None
