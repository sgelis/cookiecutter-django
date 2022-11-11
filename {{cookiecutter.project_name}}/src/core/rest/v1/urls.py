# Django
from django.urls import path

# Own
from . import views

app_name = "core.rest"


urlpatterns = [
    path("ping/", views.Ping.as_view(), name="ping"),
]
