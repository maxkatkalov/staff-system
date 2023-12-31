# Generated by Django 4.2.5 on 2023-10-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "staff_app",
            "0006_alter_company_foundation_date_alter_position_name",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="country_registry",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="position",
            name="name",
            field=models.CharField(
                default="Unnamed position 2023-10-02 07:31:23.268048",
                max_length=156,
                unique=True,
            ),
        ),
    ]
