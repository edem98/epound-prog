# Generated by Django 2.1.1 on 2018-10-14 08:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0025_auto_20181014_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 3, 8, 6, 35, 278180), verbose_name="Date d'expiration"),
        ),
    ]
