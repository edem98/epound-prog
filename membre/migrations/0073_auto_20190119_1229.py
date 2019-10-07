# Generated by Django 2.1.2 on 2019-01-19 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0072_auto_20190119_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='entreprisecommerciale',
            name='date_creation',
            field=models.DateField(blank=True, max_length=100, null=True, verbose_name='Date Création'),
        ),
        migrations.AddField(
            model_name='entreprisecommerciale',
            name='num_cfe',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro CFE'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 8, 12, 29, 13, 45299), verbose_name="Date d'expiration"),
        ),
    ]
