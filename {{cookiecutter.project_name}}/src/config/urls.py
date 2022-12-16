# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

# Third party
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Own
from auth import views as custom_auth_views

urlpatterns = [
    path("api/v1/core/", include("core.rest.v1.urls", namespace="v1")),
    path("api/v1/doc/", SpectacularSwaggerView.as_view(url_name="rest_schema"), name="swagger_doc"),
    path("api/v1/schema/", SpectacularAPIView.as_view(api_version="v1"), name="rest_schema"),
    path("api/login/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("management/", admin.site.urls),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        custom_auth_views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # This path absolutely needs to come last, otherwise Angular will block access to all other paths
    path("", include("core.urls")),
]


if settings.DEBUG:
    # Correct URLs to serve media in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        # Third party
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
