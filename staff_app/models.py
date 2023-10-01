from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    COMPANY_STAFF_SIZE_CHOICES = (
        ('1-50', '1-50'),
        ('51-100', '51-100'),
        ('101-500', '101-500'),
        ('501+', '501+'),
    )

    name = models.CharField(max_length=63)
    foundation_date = models.DateField()
    created_at_staff = models.DateField(auto_now_add=True)
    copmany_staff_size = models.CharField(
        max_length=10,
        choices=COMPANY_STAFF_SIZE_CHOICES,
        default='1-50'
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=63)
    #TODO: add choices for this fields
    city = models.CharField(max_length=110)
    country = models.CharField(max_length=110)
    address = models.CharField(max_length=255)
    workspaces = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}, {self.city}"


class Department(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "StaffUser",
        on_delete=models.CASCADE,
        related_name="department_owner"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(
        max_length=156,
        unique=True,
        default=f"Unnamed position {datetime.now()}"
    )
    department = models.ManyToManyField(Department, related_name="positions")


class StaffUser(AbstractUser):
    owner = models.BooleanField(default=False)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="position_employees"
    )
    reporting_to = models.ForeignKey(
        "StaffUser",
        related_name="reporters",
        null=True,
        on_delete=models.CASCADE
    )
    salary = models.IntegerField(null=True)
    office = models.ForeignKey(
        Office,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    fire_date = models.DateField(default=None, null=True)
    retirement_date = models.DateField(default=None, null=True)
    last_salary_review = models.DateField(default=None, null=True)

    def __str__(self) -> str:
        return f"{self.username}"

