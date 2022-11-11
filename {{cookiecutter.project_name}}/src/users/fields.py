# Standard library
from typing import Optional

# Django
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher, make_password
from django.utils.translation import gettext


class TokenWidget(AdminTextInputWidget):
    """Simple text input with a "Generate new" button that autofills the neighboring input with a random string."""

    template_name = "users/widgets/token.html"
    input_type = "text"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({"label": gettext("No token set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({"label": gettext("Invalid token format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({"label": gettext(key), "value": value_})
        context["summary"] = summary
        return context

    class Media:
        js = (
            "admin/js/vendor/jquery/jquery.js",
            "users/js/widgets/token.js",
        )
        css = {"screen": ("users/css/widgets/token.css",)}


class TokenField(forms.CharField):
    """Stores access tokens as hashes, not plain text."""

    widget = TokenWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def to_python(self, value: Optional[str]) -> Optional[str]:
        return make_password(value, settings.SECRET_KEY)
