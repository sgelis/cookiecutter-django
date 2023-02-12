# Own
from .base import *  # noqa: F403

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path("/var") / "log" / PROJECT_SLUG / "main.log",  # noqa: F405
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 7,
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "mail_admins"],
        },
        "django.db.backends": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security.*": {
            "handlers": ["file", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["file", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "py.warnings": {
            "handlers": ["file", "mail_admins"],
            "level": "INFO",
        },
        "": {
            "handlers": ["file", "mail_admins"],
            "level": "INFO",
        },
    },
}
