# Generated by Django 2.1.1 on 2018-10-01 00:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0004_auto_20181001_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 20, 0, 27, 35, 807320), verbose_name="Date d'expiration"),
        ),
    ]
