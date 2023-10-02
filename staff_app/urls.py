from django.urls import path, include

from .views import (
    index,
    CompanyListView,
    ProfileDetailView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyDeleteView,
    StaffUserCreate,
    CompanyUpdateView,
)

app_name = "staff_app"

clientarea_urlpatterns = [
    path("", CompanyListView.as_view(), name="clientarea"),
    path("company-create/", CompanyCreateView.as_view(), name="company-create"),
    path("company-detail/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    path("company-detail/<int:pk>/create-staff/", StaffUserCreate.as_view(), name="staff-create"),
    path("company-detail/<int:pk>/delete/", CompanyDeleteView.as_view(), name="company-delete"),
    path("company-detail/<int:pk>/update/", CompanyUpdateView.as_view(), name="company-update"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="client-detail")
]

urlpatterns = [
    path("", index, name="main-page"),
    path("clientarea/", include(clientarea_urlpatterns))
]

