# Generated by Django 2.1.1 on 2018-10-18 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0033_auto_20181018_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 7, 15, 6, 8, 209660), verbose_name="Date d'expiration"),
        ),
    ]
