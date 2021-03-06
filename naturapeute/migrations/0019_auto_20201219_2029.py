# Generated by Django 3.1.2 on 2020-12-19 20:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('naturapeute', '0018_auto_20201219_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='invoice_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'author': {'city': '', 'email': '', 'iban': '', 'name': '', 'phone': '', 'rcc': '', 'street': '', 'zipcode': ''}, 'hourly_price': 0, 'services': [], 'therapist': {'city': '', 'email': '', 'name': '', 'phone': '', 'rcc': '', 'street': '', 'zipcode': ''}}, null=True),
        ),
    ]
