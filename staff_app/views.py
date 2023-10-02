from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from staff_app.models import StaffUser, Company


def index(request: HttpRequest):
    return render(request, "staff_app/index.html")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = StaffUser
    context_object_name = "staffuser"
    template_name = "staff_app/profile.html"


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = "staff_app/clientarea.html"

    def get_queryset(self):
        return get_user_model().objects.get(pk=self.request.user.pk).companies.all()
