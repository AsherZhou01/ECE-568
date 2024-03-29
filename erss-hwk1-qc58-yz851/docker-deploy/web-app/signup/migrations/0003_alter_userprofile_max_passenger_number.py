# Generated by Django 4.2 on 2024-02-02 01:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signup", "0002_alter_userprofile_license_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="max_passenger_number",
            field=models.PositiveIntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(8),
                ],
            ),
        ),
    ]
