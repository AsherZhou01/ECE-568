# Generated by Django 4.2 on 2024-02-08 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signup", "0014_alter_userprofile_vehicle_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trip",
            name="vehicle_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("any", "Any"),
                    ("economy", "Economy"),
                    ("comfort", "Comfort"),
                    ("luxury", "Luxury"),
                    ("suv", "SUV"),
                ],
                default="economy",
                max_length=20,
            ),
        ),
    ]
