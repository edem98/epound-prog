# Generated by Django 2.1.1 on 2018-10-27 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0047_auto_20181025_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 16, 15, 10, 44, 938824), verbose_name="Date d'expiration"),
        ),
    ]
