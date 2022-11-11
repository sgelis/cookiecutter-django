# Standard library
from typing import List, Union

# Django
from django.conf import settings
from django.urls import URLPattern, URLResolver, path

# Own
from . import views

app_name = "core"


urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("", views.index, name="index"),
    path("browserconfig.xml", views.browserconfig_xml, name="browserconfig_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("site.webmanifest", views.site_webmanifest, name="site_webmanifest"),
]

if settings.DEBUG:
    urlpatterns += [
        path("400/", views.http400, name="http400", kwargs={"exception": Exception("Bad request")}),
        path("403/", views.http403, name="http403", kwargs={"exception": Exception("Permission denied")}),
        path("404/", views.http404, name="http404", kwargs={"exception": Exception("Not found")}),
        path("500/", views.http500, name="http500", kwargs={"exception": Exception("Internal server error")}),
    ]
