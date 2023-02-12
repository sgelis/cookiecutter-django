# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth"
    label = "custom_auth"
    verbose_name = _("Authentication")

    def ready(self) -> None:
        super().ready()
        # Own
        from . import signals  # noqa: F401
