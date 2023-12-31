# Generated by Django 4.2.5 on 2023-10-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "staff_app",
            "0009_remove_staffuser_company_remove_staffuser_department_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="position",
            name="name",
            field=models.CharField(
                default="Unnamed position 2023-10-02 13:47:13.900585",
                max_length=156,
                unique=True,
            ),
        ),
    ]
