# Generated by Django 2.1.2 on 2018-11-01 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0054_auto_20181101_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 21, 11, 35, 23, 86466), verbose_name="Date d'expiration"),
        ),
    ]
