from django.test import TestCase
from django.contrib.auth import get_user_model
from staff_app.models import Company, Department, StaffUser
from staff_app.forms import (
    RegistrationForm,
    CompanyForm,
    StaffUsernameUpdateForm,
    StaffNameSurnameUpdateForm,
    StaffEmailUpdateForm,
    StaffLogoUpdateForm,
    DepartmentForm,
)


class RegistrationFormTest(TestCase):
    def test_registration_form_valid(self):
        data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword456",  # Passwords do not match
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())


class CompanyFormTest(TestCase):
    def test_company_form_valid(self):
        data = {
            "name": "Test Company",
            "foundation_date": "2023-01-01",
            "copmany_staff_size": "1-50",
            "description": "Test description",
            "country_registry": "Test country",
        }
        form = CompanyForm(data=data)
        self.assertTrue(form.is_valid())

    def test_company_form_invalid(self):
        data = {
            "name": "Test Company",
            "foundation_date": "2023-01-01",
            "copmany_staff_size": "Invalid Choice",  # Invalid choice
            "description": "Test description",
            "country_registry": "Test country",
        }
        form = CompanyForm(data=data)
        self.assertFalse(form.is_valid())


class StaffUsernameUpdateFormTest(TestCase):
    def test_staff_username_update_form_valid(self):
        data = {
            "username": "new_username",
        }
        form = StaffUsernameUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_staff_username_update_form_invalid(self):
        data = {
            "username": "",  # Username is required
        }
        form = StaffUsernameUpdateForm(data=data)
        self.assertFalse(form.is_valid())
