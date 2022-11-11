# Django
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.template import loader
from django.utils.translation import gettext_lazy as _


def browserconfig_xml(request: HttpRequest) -> HttpResponse:
    return render(request, "{{ cookiecutter.project_slug }}/browserconfig.xml")


def http400(request: HttpRequest, exception=None, template_name=None) -> HttpResponseBadRequest:
    template400 = loader.get_template("core/400.html")
    return HttpResponseBadRequest(template400.render(request=request, context={"exception": str(exception)}))


def http403(request: HttpRequest, exception=None, template_name=None) -> HttpResponseForbidden:
    template403 = loader.get_template("core/403.html")
    return HttpResponseForbidden(template403.render(request=request, context={"exception": str(exception)}))


def http404(request: HttpRequest, exception=None, template_name=None) -> HttpResponseNotFound:
    template404 = loader.get_template("core/404.html")
    return HttpResponseNotFound(template404.render(request=request, context={"exception": str(exception)}))


def http500(request: HttpRequest, exception=None, template_name=None) -> HttpResponseServerError:
    template500 = loader.get_template("core/500.html")
    return HttpResponseServerError(template500.render(request=request, context={"exception": str(exception)}))


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "title": _("Home"),
    }
    return render(request, "core/index.html", context)


def robots_txt(request: HttpRequest) -> HttpResponse:
    return render(request, "{{ cookiecutter.project_slug }}/robots.txt")


def site_webmanifest(request: HttpRequest) -> HttpResponse:
    return render(request, "{{ cookiecutter.project_slug }}/site.webmanifest")
