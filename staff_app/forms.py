from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # Import get_user_model

from .models import Company, Department, StaffUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = (
            "name",
            "foundation_date",
            "copmany_staff_size",
            "description",
            "country_registry",
            "logo",
        )


class StaffUsernameUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)


class StaffNameSurnameUpdateForm(ModelForm):
    class Meta:
        model = StaffUser
        fields = ("first_name", "last_name")


class StaffEmailUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)


class StaffLogoUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("logo",)


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ("name", "description")
