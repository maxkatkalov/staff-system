from django.urls import path, include

from .views import index, clientarea, ProfileDetailView

app_name = "staff_app"

clientarea_urlpatterns = [
    path("", clientarea, name="clientarea"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="client-detail")
]

urlpatterns = [
    path("", index, name="main-page"),
    path("clientarea/", include(clientarea_urlpatterns))
]

