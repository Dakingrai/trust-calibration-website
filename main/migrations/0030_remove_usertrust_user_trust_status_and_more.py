# Generated by Django 4.2.4 on 2023-10-13 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0029_jiantrustscale"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usertrust",
            name="user_trust_status",
        ),
        migrations.AddField(
            model_name="usertrust",
            name="most_part_i_distrust",
            field=models.IntegerField(
                choices=[(0, "Low"), (1, "Mid"), (2, "High")], default=0
            ),
        ),
        migrations.AddField(
            model_name="usertrust",
            name="tendency_to_trust",
            field=models.IntegerField(
                choices=[(0, "Low"), (1, "Mid"), (2, "High")], default=0
            ),
        ),
        migrations.AddField(
            model_name="usertrust",
            name="trust_unitl_no_reason",
            field=models.IntegerField(
                choices=[(0, "Low"), (1, "Mid"), (2, "High")], default=0
            ),
        ),
        migrations.CreateModel(
            name="UserDemographic",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Others")],
                        max_length=100,
                        null=True,
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