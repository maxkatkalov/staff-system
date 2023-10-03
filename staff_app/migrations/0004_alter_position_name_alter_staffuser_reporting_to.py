# Generated by Django 4.2.5 on 2023-10-01 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("staff_app", "0003_alter_position_name_alter_staffuser_fire_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="position",
            name="name",
            field=models.CharField(
                default="Unnamed position 2023-10-01 15:26:42.439776",
                max_length=156,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="staffuser",
            name="reporting_to",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reporters",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
