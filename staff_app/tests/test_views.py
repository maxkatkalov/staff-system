from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from staff_app.models import Company, Department, StaffUser, Office, Position
from staff_app.forms import RegistrationForm


class ViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_index_view(self):
        response = self.client.get(reverse("staff_app:main-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "staff_app/index.html")

    def test_login_test_user_view(self):
        response = self.client.get(reverse("staff_app:clientarea"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="testuser", password="testpassword")
        self.assertEqual(response.status_code, 302)

    def test_clientarea_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("staff_app:clientarea"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "staff_app/clientarea.html")

    def test_profile_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        user = get_user_model().objects.get(username="testuser")
        response = self.client.get(
            reverse("staff_app:client-detail", args=[user.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "staff_app/profile.html")

    def test_company_create_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("staff_app:company-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "staff_app/compnay-creation.html")

    def test_company_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        company = Company.objects.create(name="Test Company")
        response = self.client.get(
            reverse("staff_app:company-detail", args=[company.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "staff_app/company-detail.html")

    def test_registration_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        form = RegistrationForm()
        data = {
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)
