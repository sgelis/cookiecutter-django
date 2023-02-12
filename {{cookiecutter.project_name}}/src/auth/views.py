# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import HttpResponse

# Third party
from axes.utils import reset as axes_reset

User = get_user_model()


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Resets `axes` `AccessAttempt`s after password reset was confirmed."""

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        user = form.save()
        axes_reset(username=user.username)  # type: ignore[attr-defined]  # "AbstractBaseUser" has no attribute "username"  # noqa: E501
        return super().form_valid(form)
