from django.test import TestCase
from staff_app.models import Company, Office, Department, Position, StaffUser
from django.contrib.auth import get_user_model
from datetime import date


class CompanyModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_company_creation(self):
        company = Company.objects.create(
            owner=self.user,
            name="Test Company",
            foundation_date=date(2000, 1, 1),
            copmany_staff_size="1-50",
            description="Test description",
            country_registry="Test country",
        )
        self.assertEqual(company.__str__(), "Test Company")
        self.assertEqual(
            company.get_absolute_url(),
            f"/clientarea/company-detail/{company.pk}/",
        )


class OfficeModelTest(TestCase):
    def test_office_creation(self):
        company = Company.objects.create(
            name="Test Company",
        )
        office = Office.objects.create(
            name="Test Office",
            city="Test City",
            country="Test Country",
            address="Test Address",
            workspaces=10,
            description="Test description",
            company=company,
            opened=date(2023, 1, 1),
        )
        self.assertEqual(office.__str__(), "Test Office, Test City")


class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        company = Company.objects.create(
            name="Test Company",
        )
        department = Department.objects.create(
            name="Test Department",
            company=company,
            description="Test description",
        )
        self.assertEqual(department.__str__(), "Test Department")
        self.assertEqual(
            department.get_absolute_url(),
            f"/clientarea/company-detail/{company.pk}/departments/{department.pk}/",
        )


class PositionModelTest(TestCase):
    def test_position_creation(self):
        company = Company.objects.create(
            name="Test Company",
        )
        department = Department.objects.create(
            name="Test Department",
            company=company,
        )
        position = Position.objects.create(
            name="Test Position",
            department=department,
            description="Test description",
        )
        self.assertEqual(position.__str__(), "Test Position")
        self.assertEqual(
            position.get_absolute_url(),
            f"/clientarea/company-detail/{position.pk}/departments/{company.pk}/positions/{department.pk}/",
        )


class StaffUserModelTest(TestCase):
    def test_staff_user_creation(self):
        staff_user = StaffUser.objects.create(
            username="testuser",
            password="testpassword",
        )
        self.assertEqual(staff_user.__str__(), "testuser")
        self.assertEqual(
            staff_user.get_absolute_url(), f"/clientarea/{staff_user.pk}/"
        )
