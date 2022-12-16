# Django
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Third party
from csp.decorators import csp_exempt


def browserconfig_xml(request: HttpRequest) -> HttpResponse:
    return render(request, "{{ cookiecutter.project_slug }}/browserconfig.xml", content_type="text/xml")


@csp_exempt
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "core/index.html")


def robots_txt(request: HttpRequest) -> HttpResponse:
    return render(request, "{{ cookiecutter.project_slug }}/robots.txt", content_type="text/plain")


def site_webmanifest(request: HttpRequest) -> HttpResponse:
    return render(request, "{{ cookiecutter.project_slug }}/site.webmanifest", content_type="application/manifest+json")
