# Generated by Django 4.2.4 on 2023-09-19 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0020_usertransaprency_user_transparency"),
    ]

    operations = [
        migrations.AddField(
            model_name="study",
            name="is_training_sample",
            field=models.BooleanField(default=False),
        ),
    ]
