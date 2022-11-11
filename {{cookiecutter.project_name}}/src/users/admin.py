# Standard library
from typing import List, Optional

# Django
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

# Own
from utils.typing import AuthenticatedWSGIRequest
from .forms import CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "password1", "password2")}),)
    fieldsets = (  # type: ignore[assignment]  # stubs issue
        (None, {"fields": ("username", "password", "access_token")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Settings"), {"fields": ("language",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "first_name", "last_name", "is_staff")
    search_fields = ("username", "first_name", "last_name")
    ordering = ("username",)

    def get_fieldsets(self, request: AuthenticatedWSGIRequest, obj: Optional[User] = None):  # type: ignore[override]
        """Filters visible fieldsets depending on requesting user permissions."""
        fieldsets = super().get_fieldsets(request, obj)

        if not request.user.has_perm("users.view_whole_user_form"):
            fieldsets = fieldsets[:-2]

        return fieldsets

    def get_queryset(self, request: AuthenticatedWSGIRequest) -> QuerySet:  # type: ignore[override]
        """Filters visible users QuerySet depending on requesting user permissions."""
        if request.user.is_superuser:
            qs = User.objects.all()
        elif request.user.has_perm("users.view_all_users"):
            qs = User.objects.exclude(is_superuser=True)
        else:
            qs = User.objects.filter(pk=request.user.pk)

        return qs

    def get_readonly_fields(  # type: ignore[override]
        self, request: AuthenticatedWSGIRequest, obj: Optional[User] = None
    ) -> List[str]:
        """Makes the `is_superuser` boolean editable **ONLY** by superusers."""
        ro_fields = list(super().get_readonly_fields(request, obj))

        if not request.user.is_superuser:
            ro_fields.append("is_superuser")

        return ro_fields

    def has_change_permission(  # type: ignore[override]
        self, request: AuthenticatedWSGIRequest, obj: Optional[User] = None
    ) -> bool:
        """Allows editing a user depending on requesting user permissions (self-edit only or global edit)."""
        super_perm = super().has_change_permission(request, obj)

        if request.user.has_perm("users.change_all_users"):
            custom_perm = True

        else:
            if obj is not None and obj.pk == request.user.pk:
                custom_perm = True
            else:
                custom_perm = False

        return super_perm and custom_perm

    def response_change(self, request: HttpRequest, obj: User) -> HttpResponse:
        """Applies user language right after user edit."""
        response = super().response_change(request, obj)

        # Only if user is self-editing
        if request.user == obj:
            translation.activate(obj.language)
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, obj.language, secure=settings.LANGUAGE_COOKIE_SECURE, samesite="Lax"
            )

        return response
