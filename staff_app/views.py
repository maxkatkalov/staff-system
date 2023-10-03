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
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from staff_app.models import (
    StaffUser,
    Company,
    Department,
    Position,
    Office,
)

from staff_app.forms import CompanyForm, StaffUserCreateForm, DepartmentForm


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


class CompanyDetailView(DetailView, MultipleObjectMixin):
    model = Company
    template_name = "staff_app/company-detail.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        departments = self.object.departments.all()
        context = super().get_context_data(object_list=departments, **kwargs)
        return context


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("staff_app:clientarea")


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = "staff_app/clientarea.html"
    paginate_by = 5

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


class DepartmentListView(ListView):
    model = Department
    template_name = "staff_app/department-list.html"
    paginate_by = 5


class PositionCreateView(CreateView):
    model = Position
    fields = ("name", "description")
    template_name = "staff_app/position-creation.html"

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            Company.objects.get(
                pk=self.args["pk"]
            ).departments.get(
                pk=self.args["id"]
            ).positions.add(
                Position.objects.get(pk=self.object.pk)
            )
            return super().form_valid(form)
        return self.form_invalid(form)


class PositionDetailView(DetailView, MultipleObjectMixin):
    model = Position
    paginate_by = 5

    def get_context_data(self, **kwargs):
        departments = self.object.departments.all()
        context = super().get_context_data(object_list=departments, **kwargs)
        return context

    def get_object(self):
        return get_object_or_404(Position, pk=self.kwargs["position_id"], company_id=self.kwargs["pk"], department=Department.objects.get(pk=self.kwargs["id"]))


class PositionUpdateView(UpdateView):
    model = Position
    fields = ("name", "description")


class OfficeCreateView(CreateView):
    model = Office
    fields = ["name", "city", "country", "address", "workspaces", "description"]

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            form.instance.company.add(Company.objects.get(pk=self.kwargs["pk"]))
            if self.kwargs.get("id"):
                Department.objects.get(pk=self.kwargs["id"]).department_offices.add(self.object)
            return super().form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("staff_app:office-detail", kwargs={"pk": self.kwargs["pk"], "office_id": self.object.pk})


class OfficeUpdateView(UpdateView):
    model = Office
    fields = "__all__"
    success_url = reverse_lazy("staff_app:clientarea")

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["office_id"], company=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("staff_app:office-detail", kwargs={"pk": self.kwargs["pk"], "office_id": self.object.pk})


class OfficeDetailView(DetailView):
    model = Office

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["office_id"], company=self.kwargs["pk"])


class OfficeDeleteView(DeleteView):
    model = Office
    success_url = reverse_lazy("staff_app:clientarea")

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["office_id"], company=self.kwargs["pk"])


class StaffUserCreate(CreateView):
    model = StaffUser
    form_class = StaffUserCreateForm
    template_name = "staff_app/client-create.html"
    success_url = reverse_lazy("staff_app:clientarea")