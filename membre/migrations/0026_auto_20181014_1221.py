# Generated by Django 2.1.1 on 2018-10-14 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0025_auto_20181014_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 3, 12, 21, 29, 874798), verbose_name="Date d'expiration"),
        ),
    ]
