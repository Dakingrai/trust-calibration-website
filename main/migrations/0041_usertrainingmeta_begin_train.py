# Generated by Django 4.2.4 on 2024-01-22 15:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0040_usertrainingmeta_general_task"),
    ]

    operations = [
        migrations.AddField(
            model_name="usertrainingmeta",
            name="begin_train",
            field=models.BooleanField(default=False),
        ),
    ]
