# Standard library
from typing import List, Optional, Union

# Django
from django.conf import settings
from django.contrib import admin, auth
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import URLPattern, URLResolver, path
from django.utils import translation

# Own
from utils.typing import AuthenticatedWSGIRequest
from .autocomplete import SimplerAutocompleteJsonView


class CustomAdminSite(admin.sites.AdminSite):
    site_title = "{{ cookiecutter.project_name }}"
    site_header = "{{ cookiecutter.project_name }}"

    def get_urls(self) -> List[Union[URLResolver, URLPattern]]:
        """Adds custom URLs to default admin URLs."""
        custom_urls: List[Union[URLResolver, URLPattern]] = [
            path("autocomplete/simpler/", self.admin_view(self.simpler_autocomplete_view), name="simpler_autocomplete"),
        ]

        return custom_urls + super().get_urls()

    def index(  # type: ignore[override]
        self, request: AuthenticatedWSGIRequest, extra_context: Optional[dict] = None
    ) -> HttpResponse:
        """Applies user language."""
        response = super().index(request, extra_context)
        user = auth.get_user(request)

        if not isinstance(user, AnonymousUser):
            language = getattr(user, "language")
            translation.activate(language)
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, language, secure=settings.LANGUAGE_COOKIE_SECURE, samesite="Lax"
            )

        return response

    def login(self, request: HttpRequest, extra_context: Optional[dict] = None) -> HttpResponse:
        """Applies user language."""
        response = super().login(request, extra_context)

        user = auth.get_user(request)
        if not isinstance(user, AnonymousUser):
            language = getattr(user, "language")
            translation.activate(language)
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, language, secure=settings.LANGUAGE_COOKIE_SECURE, samesite="Lax"
            )

        return response

    def simpler_autocomplete_view(self, request: AuthenticatedWSGIRequest) -> JsonResponse:
        return SimplerAutocompleteJsonView.as_view(admin_site=self)(request)  # type: ignore[return-value]  # being more specific than parent here  # noqa: E501
