# Generated by Django 4.2 on 2024-02-02 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signup", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="license_number",
            field=models.CharField(default="", max_length=20),
        ),
    ]
