from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpRequest
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from staff_app.models import StaffUser, Company, Department
from .forms import (
    CompanyForm,
    StaffUserCreateForm,
    DepartmentForm
)


def index(request: HttpRequest):
    return render(request, "staff_app/index.html")


class ProfileDetailView(DetailView):
    model = StaffUser
    context_object_name = "staffuser"
    template_name = "staff_app/profile.html"


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "staff_app/compnay-creation.html"
    success_url = reverse_lazy("staff_app:clientarea")

    def form_valid(self, form):
        # Set the 'owner' field to the currently logged-in user's ID
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "staff_app/company-update.html"

    def get_success_url(self):
        updated_company = self.object

        return updated_company.get_absolute_url()


class CompanyDetailView(DetailView):
    model = Company
    template_name = "staff_app/company-detail.html"


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("staff_app:clientarea")


class CompanyListView(ListView):
    model = Company
    template_name = "staff_app/clientarea.html"

    def get_queryset(self):
        return get_user_model().objects.get(pk=self.request.user.pk).companies.all()


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "staff_app/department-creation.html"

    def form_valid(self, form):
        # Set the 'company' field to the certain company where this view called
        form.instance.company = Company.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "staff_app/department-update.html"

    def get_object(self):
        return get_object_or_404(Department, pk=self.kwargs["id"], company_id=self.kwargs["pk"])

    def get_success_url(self):
        return self.object.get_absolute_url()


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "staff_app/department-detail.html"

    def get_object(self):
        return get_object_or_404(Department, pk=self.kwargs["id"], company_id=self.kwargs["pk"])

    def get_success_url(self):
        return self.object.get_absolute_url()


class StaffUserCreate(CreateView):
    model = StaffUser
    form_class = StaffUserCreateForm
    template_name = "staff_app/client-create.html"
    success_url = reverse_lazy("staff_app:clientarea")
