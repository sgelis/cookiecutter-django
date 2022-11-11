# Standard library
from typing import Optional

# Django
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _


class Settings(models.Model):
    def __str__(self):
        return gettext("settings")

    class Meta:
        verbose_name = _("settings")
        verbose_name_plural = _("settings")


class CachedSettings:
    """Caches settings to minimize the number of SQL requests on that frequently required object.

    The first (and only) SQL request is sent on the first instantiation of the class, not before. Subsequent
    instantiations of this class return cached settings.
    """

    _settings = None

    def __new__(cls) -> Settings:  # type: ignore[misc]  # returning instance of `Settings` class on purpose
        cls._settings = cls._settings or Settings.objects.first()
        return cls._settings  # type: ignore[return-value]  # at this point, cls._settings is guaranteed to be not-None

    @classmethod
    def clear_cache(cls):
        """Clears cache such that a new instantation of this class will trigger a new SQL request to fetch the
        object from DB."""
        cls._settings = None
