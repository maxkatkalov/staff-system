from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.conf import settings


class Company(models.Model):
    COMPANY_STAFF_SIZE_CHOICES = (
        ('1-50', '1-50'),
        ('51-100', '51-100'),
        ('101-500', '101-500'),
        ('501+', '501+'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="companies", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    foundation_date = models.DateField(null=True, blank=True)
    created_at_staff = models.DateField(auto_now_add=True)
    copmany_staff_size = models.CharField(
        max_length=10,
        choices=COMPANY_STAFF_SIZE_CHOICES,
        default='1-50'
    )
    description = models.TextField(null=True, blank=True)
    country_registry = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to="images/company/logos", null=True, blank=True)

    def get_absolute_url(self):
        return reverse("staff_app:company-detail", args=[self.pk])

    def __str__(self) -> str:
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=63)
    city = models.CharField(max_length=110)
    country = models.CharField(max_length=110)
    address = models.CharField(max_length=255)
    workspaces = models.IntegerField()
    description = models.TextField()
    company = models.ManyToManyField(Company, related_name="company_offices")

    def __str__(self) -> str:
        return f"{self.name}, {self.city}"

    def get_absolute_url(self):
        return reverse("staff_app:office-detail", kwargs={"office_id": self.pk})


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments"
    )
    description = models.TextField(null=True, blank=True)
    created_at_staff = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("staff_app:department-detail", args=[self.company.pk, self.pk])

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(
        max_length=156,
        unique=True,
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="positions")
    description = models.TextField(null=True, blank=True)
    created_at_staff = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse(
                "staff_app:position-detail",
                kwargs={
                    "position_id": self.pk,
                    "pk": self.department.company.pk,
                    "id": self.department.pk
                },
        )


class StaffUser(AbstractUser):
    logo = models.ImageField(upload_to="images/profile/logos", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("staff_app:client-detail", args=[self.pk])
