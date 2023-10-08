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
    DepartmentCreateView,
    DepartmentUpdateView,
    DepartmentDetailView,
    DepartmentListView,
    PositionCreateView,
    PositionDetailView,
    PositionUpdateView,
    OfficeDetailView,
    OfficeCreateView,
    OfficeDeleteView,
    OfficeUpdateView,
    StaffUsernameUpdate,
    StaffNameSurnameUpdate,
    StaffEmailUpdateView,
    StaffLogoUpdateView,
    DepartmentDeleteView,
    PositionDeleteView,
    DepartmentListView,
)

app_name = "staff_app"

clientarea_urlpatterns = [
    path("", CompanyListView.as_view(), name="clientarea"),
    path(
        "company-create/", CompanyCreateView.as_view(), name="company-create"
    ),
    path(
        "company-detail/<int:pk>/",
        CompanyDetailView.as_view(),
        name="company-detail",
    ),
    path("company-detail/<int:pk>/offices/create/", OfficeCreateView.as_view(), name="office-create"),
    path("company-detail/<int:pk>/offices/<int:office_id>/", OfficeDetailView.as_view(), name="office-detail"),
    path("company-detail/<int:pk>/offices/<int:office_id>/delete/", OfficeDeleteView.as_view(), name="office-delete"),
    path("company-detail/<int:pk>/offices/<int:office_id>/update/", OfficeUpdateView.as_view(), name="office-update"),
    path(
        "company-detail/<int:pk>/departments/create",
        DepartmentCreateView.as_view(),
        name="department-create",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/delete",
        DepartmentDeleteView.as_view(),
        name="department-delete",
    ),
    path(
        "company-detail/<int:pk>/departments/",
        DepartmentListView.as_view(),
        name="department-list",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/update/",
        DepartmentUpdateView.as_view(),
        name="department-update",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/positions/create/",
        PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/positions/<int:position_id>/",
        PositionDetailView.as_view(),
        name="position-detail",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/positions/<int:position_id>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "company-detail/<int:pk>/departments/<int:id>/positions/<int:position_id>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path(
        "company-detail/<int:pk>/create-staff/",
        StaffUserCreate.as_view(),
        name="staff-create",
    ),
    path(
        "company-detail/<int:pk>/delete/",
        CompanyDeleteView.as_view(),
        name="company-delete",
    ),
    path(
        "company-detail/<int:pk>/update/",
        CompanyUpdateView.as_view(),
        name="company-update",
    ),
    path("<int:pk>/", ProfileDetailView.as_view(), name="client-detail"),
    path("<int:pk>/update-username/", StaffUsernameUpdate.as_view(), name="client-update-username"),
    path("<int:pk>/update-name-surname/", StaffNameSurnameUpdate.as_view(), name="client-update-name-surname"),
    path("<int:pk>/email-update/", StaffEmailUpdateView.as_view(), name="email-update"),
    path("<int:pk>/logo-update/", StaffLogoUpdateView.as_view(), name="logo-update"),
]

urlpatterns = [
    path("", index, name="main-page"),
    path("clientarea/", include(clientarea_urlpatterns)),
]
