# Generated by Django 5.1.4 on 2025-02-08 12:55

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
