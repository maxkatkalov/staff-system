from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Company, StaffUser, Department


class StaffCreateForm(UserCreationForm):
    class Meta:
        model = StaffUser
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "logo",
            "email",
        )


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


class StaffUsernameUpdateForm(ModelForm):
    class Meta:
        model = StaffUser
        fields = ("username",)


class StaffNameSurnameUpdateForm(ModelForm):
    class Meta:
        model = StaffUser
        fields = ("first_name", "last_name")


class StaffEmailUpdateForm(ModelForm):
    class Meta:
        model = StaffUser
        fields = ("email", )


class StaffLogoUpdateForm(ModelForm):
    class Meta:
        model = StaffUser
        fields = ("logo", )


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ("name", "description")
