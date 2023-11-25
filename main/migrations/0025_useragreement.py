# Generated by Django 4.2.4 on 2023-10-07 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0024_alter_trainingstudy_sample"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAgreement",
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
                ("user_agreement_status", models.BooleanField(default=False)),
                ("user_agreement_time", models.DateTimeField(blank=True, null=True)),
                ("user_agreement", models.TextField(blank=True, null=True)),
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
