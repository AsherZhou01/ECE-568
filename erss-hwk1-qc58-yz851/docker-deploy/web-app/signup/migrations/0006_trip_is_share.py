# Generated by Django 4.2 on 2024-02-07 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signup", "0005_trip"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="is_share",
            field=models.BooleanField(default=False),
        ),
    ]
