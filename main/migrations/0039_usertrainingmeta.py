# Generated by Django 4.2.4 on 2024-01-19 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0038_alter_userdemographic_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserTrainingMeta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_two", models.BooleanField(default=False)),
                ("task_one", models.BooleanField(default=False)),
                ("question", models.BooleanField(default=False)),
                ("feedback", models.BooleanField(default=False)),
                ("database", models.BooleanField(default=False)),
                ("model_explanation", models.BooleanField(default=False)),
                ("explanation_density", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
