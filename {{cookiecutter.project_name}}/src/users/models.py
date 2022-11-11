# Standard library
from typing import List, Optional

# Django
from django.apps import apps
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Handles users whose username field is the e-mail address (no dedicated `email` field)."""

    @classmethod
    def normalize_email(cls, email: Optional[str]) -> str:
        """Normalizes the email address by lowercasing it."""
        email = email or ""
        return email.lower()

    def _create_user(self, username, password, **extra_fields):
        """Creates and saves a user with the given username and password (no e-mail)."""
        if not username:  # pragma: no cover  # already tested by Django
            raise ValueError("The given username must be set")

        # Lookup the real model class from the global src registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)  # type: ignore[attr-defined]
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:  # pragma: no cover  # already tested by Django
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:  # pragma: no cover  # already tested by Django
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    EMAIL_FIELD = "username"
    # This is required to make the `createsuperuser` management command work properly
    REQUIRED_FIELDS: List[str] = []

    objects = CustomUserManager()  # type: ignore[assignment]  # Parent type too strict, override required

    # Use an e-mail address as username
    # N.B.: the USERNAME_FIELD setting on the User model is supposed to allow this but is screws a lot of thigs up all
    #       over the place (including drf-simplejwt logic)
    username = models.EmailField(_("email address"), unique=True)
    email = None  # type: ignore[assignment]  # Not the same type as parent class
    # 156 chars is the hash size with Django 4 scrypt implementation
    password = models.CharField(_("password"), max_length=156)
    access_token = models.CharField(_("access token"), max_length=156, blank=True)
    language = models.CharField(_("language"), max_length=5, default=settings.LANGUAGE_CODE, choices=settings.LANGUAGES)

    @classmethod
    def normalize_username(cls, username):
        """Normalizes username as an e-mail address, since it is one."""
        return cls.objects.normalize_email(username) if isinstance(username, str) else username

    class Meta:
        permissions = (
            ("view_all_users", _("View all users")),
            ("change_all_users", _("Edit all users")),
            ("view_whole_user_form", _("View whole user form")),
        )
        verbose_name = _("user")
        verbose_name_plural = _("users")
