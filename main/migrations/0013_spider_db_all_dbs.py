# Generated by Django 4.2.4 on 2023-08-24 16:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0012_rename_db_schema_spider_db_column_names_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="spider_db",
            name="all_dbs",
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]