"""Main URL configuration for this django project."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        route="api-auth/",
        view=include("rest_framework.urls", namespace="rest_framework"),
    ),
    path("api/", include("app_dogs.urls")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = urlpatterns + debug_toolbar_urls()
