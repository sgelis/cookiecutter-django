# Django
from django.db import connection
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils.translation import gettext

# Third party
import pytest

# Own
from utils.typing import AuthenticatedWSGIRequest
from ..models import CachedSettings, Settings
from ..views import http400, http403, http404, http500


class TestSettingsModel:
    @pytest.mark.django_db
    def test_settings_presence(self):
        settings_qset = Settings.objects.all()
        assert settings_qset.count() == 1

    @pytest.mark.django_db
    def test_settings_str(self):
        settings_ = Settings.objects.first()
        assert str(settings_) == gettext("settings")


@pytest.mark.django_db
class TestCachedSettings:
    def test_prevents_multiple_sql_queries(self):
        # Naïve method: triggers 2 SQL queries
        with CaptureQueriesContext(connection) as ctx:
            settings_1 = Settings.objects.first()
            settings_2 = Settings.objects.first()
            assert len(ctx.captured_queries) == 2
            assert settings_1.pk == settings_2.pk
            assert settings_1 is not settings_2

        # Using cache: triggers only 1 SQL query
        CachedSettings.clear_cache()
        with CaptureQueriesContext(connection) as ctx:
            settings_1 = CachedSettings()
            settings_2 = CachedSettings()
            assert len(ctx.captured_queries) == 1
            assert settings_1.pk == settings_2.pk
            assert settings_1 is settings_2

    def test_clear_cache(self):
        CachedSettings.clear_cache()

        # Initial call => 1 SQL request
        with CaptureQueriesContext(connection) as ctx:
            CachedSettings()
            assert len(ctx.captured_queries) == 1

        # Second call => No SQL request
        with CaptureQueriesContext(connection) as ctx:
            CachedSettings()
            assert len(ctx.captured_queries) == 0

        # Cache clear + third call => 1 SQL request
        CachedSettings.clear_cache()
        with CaptureQueriesContext(connection) as ctx:
            CachedSettings()
            assert len(ctx.captured_queries) == 1


class TestSettingsAdmin:
    @pytest.mark.django_db
    def test_has_add_permission(self, rf, user_superuser, settings_admin):
        request = rf.get(reverse("admin:core_settings_changelist"))
        request.user = user_superuser
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        has_perm = settings_admin.has_add_permission(request)
        assert not has_perm

    @pytest.mark.django_db
    def test_has_delete_permission(self, rf, user_superuser, settings_admin):
        settings_ = Settings.objects.first()
        assert settings_ is not None
        request = rf.get(reverse("admin:core_settings_change", args=(settings_.pk,)))
        request.user = user_superuser
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        has_perm = settings_admin.has_delete_permission(request)
        assert not has_perm


class TestViews:
    def test_browserconfig_xml(self, client):
        response = client.get(reverse("core:browserconfig_xml"))
        assert response.status_code == 200

    def test_index(self, client):
        response = client.get(reverse("core:index"))
        assert response.status_code == 200

    def test_robots_txt(self, client):
        response = client.get(reverse("core:robots_txt"))
        assert response.status_code == 200

    def test_site_webmanifest(self, client):
        response = client.get(reverse("core:site_webmanifest"))
        assert response.status_code == 200


class TestErrorViews:
    def test_400(self, rf):
        request = rf.get(reverse("core:index"))
        response = http400(request)
        assert isinstance(response, HttpResponseBadRequest)

    def test_403(self, rf):
        request = rf.get(reverse("core:index"))
        response = http403(request)
        assert isinstance(response, HttpResponseForbidden)

    def test_404(self, rf):
        request = rf.get(reverse("core:index"))
        response = http404(request)
        assert isinstance(response, HttpResponseNotFound)

    def test_500(self, rf):
        request = rf.get(reverse("core:index"))
        response = http500(request)
        assert isinstance(response, HttpResponseServerError)
