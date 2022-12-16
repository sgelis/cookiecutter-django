# Standard library
from typing import List, Union

# Django
from django.urls import URLPattern, URLResolver, path, re_path

# Own
from . import views

app_name = "core"


urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("", views.index, name="index"),
    path("browserconfig.xml", views.browserconfig_xml, name="browserconfig_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("site.webmanifest", views.site_webmanifest, name="site_webmanifest"),
    re_path(r"^.*/$", views.index, name="index"),
]
