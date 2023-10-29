from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from staff_app.views import RegistrationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("staff_app.urls", namespace="staff_app")),
    path("accounts/register/", RegistrationView.as_view(), name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
