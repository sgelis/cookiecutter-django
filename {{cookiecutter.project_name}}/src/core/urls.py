# Standard library
from typing import List, Union

# Django
from django.urls import URLPattern, URLResolver, path, re_path
from django.views.generic import RedirectView

# Own
from . import views

app_name = "core"


urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("", RedirectView.as_view(pattern_name="core:index")),
    path("browserconfig.xml", views.browserconfig_xml, name="browserconfig_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("site.webmanifest", views.site_webmanifest, name="site_webmanifest"),
    path("app/", views.index, name="index"),
    re_path(r"^app/.*$", views.index, name="index"),
]
