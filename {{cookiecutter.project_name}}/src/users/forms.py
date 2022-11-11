# Django
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

# Own
from .fields import TokenField


class CustomUserChangeForm(UserChangeForm):
    access_token = TokenField(
        label=_("Token"),
        help_text=_("Raw tokens are not stored, so there is no way to see this user’s token."),
    )

    def clean_access_token(self):
        """If raw user input is empty, returns initial data (from DB)."""
        if self.data.get("access_token") in (None, ""):
            return self.initial.get("access_token")
        else:
            return self.cleaned_data["access_token"]
