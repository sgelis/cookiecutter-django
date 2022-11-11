# Django
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework.exceptions import PermissionDenied

# Third party
from axes.signals import user_locked_out


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    """Checks for Axes ban for API logins too.

    Raises:
        PermissionDenied: User was banned by Axes, login forbidden.
    """
    if kwargs.get("request") is not None and kwargs["request"].path == reverse("token_obtain_pair"):
        raise PermissionDenied({"code": "AXES_BAN", "detail": [_("Too many failed login attempts")]})
