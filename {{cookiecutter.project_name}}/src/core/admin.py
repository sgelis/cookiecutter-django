# Standard library
from typing import Optional

# Django
from django.contrib import admin

# Own
from utils.typing import AuthenticatedWSGIRequest
from .models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: AuthenticatedWSGIRequest) -> bool:  # type: ignore[override]
        """Forbids creating new settings."""
        return False

    def has_delete_permission(  # type: ignore[override]
        self, request: AuthenticatedWSGIRequest, obj: Optional[Settings] = None
    ) -> bool:
        """Forbids deleting existing settings."""
        return False
