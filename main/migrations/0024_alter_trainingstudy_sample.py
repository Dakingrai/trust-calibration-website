# Generated by Django 4.2.4 on 2023-09-20 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0023_trainingsamples_trainingstudy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trainingstudy",
            name="sample",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.trainingsamples"
            ),
        ),
    ]
