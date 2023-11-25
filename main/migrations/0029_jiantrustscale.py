# Generated by Django 4.2.4 on 2023-10-13 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0028_hyperparameters_agreement_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="JianTrustScale",
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
                (
                    "sytem_deceptive",
                    models.IntegerField(
                        choices=[(0, "Low"), (1, "Mid"), (2, "High")], default=0
                    ),
                ),
                (
                    "system_underhanded",
                    models.IntegerField(
                        choices=[(0, "Low"), (1, "Mid"), (2, "High")], default=0
                    ),
                ),
                (
                    "system_sus_intent",
                    models.IntegerField(
                        choices=[(0, "Low"), (1, "Mid"), (2, "High")], default=0
                    ),
                ),
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
