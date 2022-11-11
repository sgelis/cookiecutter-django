# Standard library
import logging
import os
from email.utils import parseaddr
from pathlib import Path
from typing import List

# Third party
import environ

# Django
from django.conf import global_settings

env = environ.Env(
    DEBUG=(bool, False),
    ADMINS=(list, []),
    MANAGERS=(list, []),
    ALLOWED_HOSTS=(list, []),
    EMAIL_TIMEOUT=(int, 10),
    REQUEST_LOGGING_ENABLE_COLORIZE=(bool, False),
)

VERSION: str = "0.0.0"

PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env.read_env(BASE_DIR.parent / ".env")

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ADMINS = tuple(parseaddr(email) for email in env("ADMINS"))
MANAGERS = tuple(parseaddr(email) for email in env("MANAGERS"))

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",
    "axes",
    "corsheaders",
]

CUSTOM_APPS = [
    "config.apps.CustomAdminConfig",
    "auth",
    "users",
    "core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": env.db(),
}

# Cache
# https://docs.djangoproject.com/en/4.1/topics/cache/
CACHES = {
    "default": env.cache(),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    "axes.middleware.AxesMiddleware",
    "request_logging.middleware.LoggingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "csp.context_processors.nonce",
                "core.context_processors.project_name",
                "core.context_processors.project_slug",
                "core.context_processors.version",
            ],
            "libraries": {
                "{{ cookiecutter.project_slug }}": "templatetags.{{ cookiecutter.project_slug }}",
            },
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password hash algorithms
# Use stronger scrypt as default algorithm
# https://docs.djangoproject.com/en/4.1/topics/auth/passwords/#using-scrypt-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Custom user model
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
AUTH_USER_MODEL = "users.User"

# Authentication backends
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#authentication-backends
AUTHENTICATION_BACKENDS = ["axes.backends.AxesStandaloneBackend"] + list(global_settings.AUTHENTICATION_BACKENDS)

# Login
LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "/management/"
LOGOUT_REDIRECT_URL = "admin:login"

# Django Axes
# https://django-axes.readthedocs.io/en/latest/index.html
AXES_ONLY_USER_FAILURES = True
AXES_LOCKOUT_TEMPLATE = "registration/lockout.html"
AXES_RESET_ON_SUCCESS = True

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
    ("fr-ch", "Français"),
    ("it", "Italiano"),
]
USE_TZ = True
TIME_ZONE = "Europe/Zurich"
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "compiled_static"
STATICFILES_DIRS = global_settings.STATICFILES_DIRS + [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Uploaded files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# E-mail
# https://docs.djangoproject.com/en/4.1/topics/email/
EMAIL_CONFIG = env.email()
vars().update(EMAIL_CONFIG)
EMAIL_TIMEOUT = env("EMAIL_TIMEOUT")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 63072000
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
os.environ["wsgi.url_scheme"] = "https"

# HTTP header Content-Security-Policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
CSP_DEFAULT_SRC = ("'none'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORES = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_INCLUDE_NONCE_IN = ("script-src", "style-src")

# CORS headers
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOWED_ORIGINS: List[str] = []
CORS_ALLOW_ALL_ORIGINS = False

# Django request logging
# https://github.com/Rhumbix/django-request-logging
REQUEST_LOGGING_HTTP_4XX_LOG_LEVEL = logging.WARNING
# Using color codes can mess with file logs (this is actually only useful in consoles)
REQUEST_LOGGING_ENABLE_COLORIZE = env("REQUEST_LOGGING_ENABLE_COLORIZE")
# Truncate request body logging to avoid being flooded since django-request-logging sends one log line per body line
REQUEST_LOGGING_MAX_BODY_LENGTH = 250

# Django REST Framework
# https://www.django-rest-framework.org
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "auth.rest.UserTokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.DjangoModelPermissions",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_THROTTLE_RATES": {"anon": "10/second", "user": "10/second"},
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "ALLOWED_VERSIONS": ("v1",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular
# https://drf-spectacular.readthedocs.io/en/latest/
SPECTACULAR_SETTINGS = {
    "TITLE": "REST API documentation",
    "DESCRIPTION": "",
    "VERSION": VERSION,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
}

########################################################################################################################
# CUSTOM SETTINGS
########################################################################################################################
