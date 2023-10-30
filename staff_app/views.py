import datetime

from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.views.generic import (
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    ListView,
)
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from staff_app.models import (
    StaffUser,
    Company,
    Department,
    Position,
    Office,
)

from staff_app.forms import (
    RegistrationForm,
    CompanyForm,
    DepartmentForm,
    StaffUsernameUpdateForm,
    StaffNameSurnameUpdateForm,
    StaffEmailUpdateForm,
    StaffLogoUpdateForm,
)


def index(request: HttpRequest):
    return render(request, "staff_app/index.html")


def login_test_user(request):
    user = authenticate(request, username="user36", password="GGduIU@")
    login(request, user)
    return redirect("staff_app:clientarea")


class ProfileDetailView(DetailView):
    model = StaffUser
    context_object_name = "staffuser"
    template_name = "staff_app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_companies"] = (
            Company.objects.select_related("owner")
            .filter(owner__id=self.request.user.pk)
            .order_by("-created_at_staff")[:5]
        )
        return context


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "staff_app/compnay-creation.html"
    success_url = reverse_lazy("staff_app:clientarea")

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "staff_app/company-update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class CompanyDetailView(DetailView, MultipleObjectMixin):
    model = Company
    template_name = "staff_app/company-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            object_list=self.object.departments.all(), **kwargs
        )
        context["offices_count"] = self.object.company_offices.count()
        context["departments"] = self.object.departments.all()[:5]
        context["total_departments"] = self.object.departments.count()
        return context


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("staff_app:clientarea")


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = "staff_app/clientarea.html"
    context_object_name = "companies_list"
    paginate_by = 3

    def get_queryset(self):
        return Company.objects.prefetch_related(
            "company_offices", "departments"
        ).filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = self.get_queryset()
        context["departments_count"] = {
            company.pk: company.departments.count() for company in companies
        }
        context["offices_count"] = {
            company.pk: company.company_offices.count()
            for company in companies
        }
        context["company_exists"] = {
            company.pk: (datetime.date.today() - company.created_at_staff).days
            + 1
            for company in companies
        }
        context["total_companies"] = companies.count()
        return context


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class DepartmentDeleteView(DeleteView):
    model = Department

    def get_object(self):
        return get_object_or_404(
            Department, pk=self.kwargs["id"], company_id=self.kwargs["pk"]
        )

    def get_success_url(self):
        return reverse_lazy(
            "staff_app:department-list",
            kwargs={"pk": self.kwargs["pk"]},
        )


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm

    def get_object(self):
        return get_object_or_404(
            Department, pk=self.kwargs["id"], company_id=self.kwargs["pk"]
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class DepartmentDetailView(DetailView, MultipleObjectMixin):
    model = Department
    context_object_name = "department"

    def get_object(self):
        return get_object_or_404(
            Department, pk=self.kwargs["id"], company_id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            object_list=self.object.positions.all(), **kwargs
        )
        context["positions_count"] = self.object.positions.count()
        context["positions"] = self.object.positions.all()[:5]
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class DepartmentListView(ListView):
    model = Department
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.select_related("company").filter(
            company__pk=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = Company.objects.get(pk=self.kwargs["pk"])
        context["total_departments"] = context["company"].departments.count()
        return context


class PositionCreateView(CreateView):
    model = Position
    fields = ("name", "description")

    def form_valid(self, form):
        form.instance.department = Company.objects.get(
            pk=self.kwargs["pk"]
        ).departments.get(pk=self.kwargs["id"])

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PositionDetailView(DetailView):
    model = Position

    def get_object(self):
        return get_object_or_404(
            Position,
            pk=self.kwargs["position_id"],
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class PositionListView(ListView):
    model = Position
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.select_related("department").filter(
            department_id=self.kwargs["id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["department"] = (
            Department.objects.select_related(
                "company",
            )
            .prefetch_related("positions")
            .get(pk=self.kwargs["id"])
        )
        context["department_total_positions"] = context[
            "department"
        ].positions.count()
        return context


class PositionUpdateView(UpdateView):
    model = Position
    fields = ("name", "description")

    def get_object(self):
        return get_object_or_404(
            Position,
            pk=self.kwargs["position_id"],
        )

    def get_success_url(self):
        return self.object.get_absolute_url()


class PositionDeleteView(DeleteView):
    model = Position

    def get_object(self):
        return get_object_or_404(
            Position,
            pk=self.kwargs["position_id"],
        )

    def get_success_url(self):
        return self.object.department.get_absolute_url()


class OfficeCreateView(CreateView):
    model = Office
    fields = [
        "name",
        "city",
        "country",
        "address",
        "workspaces",
        "description",
    ]

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "staff_app:office-detail",
            kwargs={"pk": self.kwargs["pk"], "office_id": self.object.pk},
        )


class OfficeUpdateView(UpdateView):
    model = Office
    fields = [
        "name",
        "city",
        "country",
        "address",
        "workspaces",
        "description",
        "company",
    ]
    success_url = reverse_lazy("staff_app:clientarea")

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs["office_id"], company=self.kwargs["pk"]
        )

    def get_success_url(self):
        return reverse_lazy(
            "staff_app:office-detail",
            kwargs={"pk": self.kwargs["pk"], "office_id": self.object.pk},
        )


class OfficeDetailView(DetailView):
    model = Office

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs["office_id"], company=self.kwargs["pk"]
        )


class OfficeListView(ListView):
    model = Office
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.filter(company__pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = Company.objects.get(pk=self.kwargs["pk"])
        context["total_offices"] = context["company"].company_offices.count()
        return context


class OfficeDeleteView(DeleteView):
    model = Office
    success_url = reverse_lazy("staff_app:clientarea")

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs["office_id"], company=self.kwargs["pk"]
        )


class RegistrationView(CreateView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("staff_app:clientarea")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class StaffUsernameUpdate(UpdateView):
    model = StaffUser
    form_class = StaffUsernameUpdateForm
    template_name = "staff_app/staffuser_update_forms/username-update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class StaffNameSurnameUpdate(UpdateView):
    model = StaffUser
    form_class = StaffNameSurnameUpdateForm
    template_name = "staff_app/staffuser_update_forms/name-surname.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class StaffEmailUpdateView(UpdateView):
    model = StaffUser
    form_class = StaffEmailUpdateForm
    template_name = "staff_app/staffuser_update_forms/email.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class StaffLogoUpdateView(UpdateView):
    model = StaffUser
    form_class = StaffLogoUpdateForm
    template_name = "staff_app/staffuser_update_forms/logo.html"

    def get_success_url(self):
        return self.object.get_absolute_url()
