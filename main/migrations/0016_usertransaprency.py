# Generated by Django 4.2.4 on 2023-08-31 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0015_alter_study_created_alter_study_updated"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserTransaprency",
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
                ("user_id", models.IntegerField()),
                ("UserTransaprency", models.CharField(default="Low", max_length=100)),
            ],
        ),
    ]