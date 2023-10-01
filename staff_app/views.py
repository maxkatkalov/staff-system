from django.shortcuts import render, reverse
from django.http import HttpRequest
from django.views.generic import DetailView

from staff_app.models import StaffUser


def index(request: HttpRequest):
    return render(request, "staff_app/index.html")


def clientarea(request: HttpRequest):
    return render(request, "clientarea-base.html")


class ProfileDetailView(DetailView):
    model = StaffUser
    context_object_name = "staffuser"
    template_name = "staff_app/profile.html"
