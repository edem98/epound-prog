# Generated by Django 2.1.1 on 2018-10-06 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0023_auto_20181006_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 25, 0, 46, 38, 654455), verbose_name="Date d'expiration"),
        ),
    ]
