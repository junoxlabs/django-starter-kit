import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("anymail/", include("anymail.urls")),
    path("api/v1/", include("apps.api.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth_mfa.urls")),
    path("", include("pages.urls")),
]