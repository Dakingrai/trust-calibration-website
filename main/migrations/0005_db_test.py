# Generated by Django 3.2.18 on 2023-04-10 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20230408_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='db_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_db', models.TextField()),
            ],
        ),
    ]
