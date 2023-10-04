from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Company, StaffUser, Department


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = (
            "name",
            "foundation_date",
            "copmany_staff_size",
            "description",
            "country_registry",
            "logo"
        )


class StaffUserCreateForm(UserCreationForm):
    class Meta:
        model = StaffUser
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ("name", "description")
