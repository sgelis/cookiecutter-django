# Standard library
from typing import Dict

# Django
from django.conf import settings
from django.http import HttpRequest


def project_name(request: HttpRequest) -> Dict[str, str]:
    return {"project_name": settings.PROJECT_NAME}


def project_slug(request: HttpRequest) -> Dict[str, str]:
    return {"project_slug": settings.PROJECT_SLUG}


def version(request: HttpRequest) -> Dict[str, str]:
    return {"version": settings.VERSION}
