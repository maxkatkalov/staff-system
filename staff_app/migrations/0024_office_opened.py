# Generated by Django 4.2.5 on 2023-10-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("staff_app", "0023_remove_office_company_office_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="office",
            name="opened",
            field=models.DateField(blank=True, null=True),
        ),
    ]