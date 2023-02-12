# Standard library
import socket

# Own
from .base import *  # noqa: F403

INSTALLED_APPS = (
    ["whitenoise.runserver_nostatic"] + INSTALLED_APPS + ["debug_toolbar", "django_extensions"]  # noqa: F405
)
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
hostname, __, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "localhost"]
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ("debug_toolbar.panels.redirects.RedirectsPanel",),
    "SHOW_TEMPLATE_CONTEXT": True,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR.parent / "log" / "main.log",  # noqa: F405
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 7,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "file"]},
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.security.*": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "py.warnings": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    },
}
