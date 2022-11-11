# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest

# Own
from users.models import User


class AuthenticatedHttpRequest(HttpRequest):
    """
    This class should be used for typing purpose instead of `HttpRequest` where incoming request is guaranteed to be
    triggered by an authenticated user (e.g. in admin methods or in views protected by the `login_required` decorator).
    """

    user: User

    @classmethod
    def from_HttpRequest(cls, request: HttpRequest) -> "AuthenticatedHttpRequest":
        if not isinstance(request.user, User):
            raise TypeError(f"Expected User instance, got <{type(request.user)}>")
        authenticated_request = cls()
        authenticated_request.user = request.user
        return authenticated_request


class AuthenticatedWSGIRequest(WSGIRequest):
    """
    This class should be used for typing purpose instead of `WSGIRequest` where incoming request is guaranteed to be
    triggered by an authenticated user (e.g. in admin methods or in views protected by the `login_required` decorator).
    """

    user: User

    @classmethod
    def from_WSGIRequest(cls, request: WSGIRequest) -> "AuthenticatedWSGIRequest":
        if not isinstance(request.user, User):
            raise TypeError(f"Expected User instance, got <{type(request.user)}>")
        authenticated_request = cls(request.environ)
        authenticated_request.user = request.user
        return authenticated_request
