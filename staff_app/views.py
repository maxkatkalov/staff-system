from django.shortcuts import render
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

from staff_app.models import StaffUser, Company
from .forms import CompanyForm, StaffUserCreateForm


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


class StaffUserCreate(CreateView):
    model = StaffUser
    form_class = StaffUserCreateForm
    template_name = "staff_app/client-create.html"
    success_url = reverse_lazy("staff_app:clientarea")
