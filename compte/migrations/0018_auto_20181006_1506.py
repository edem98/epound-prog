# Generated by Django 2.1.1 on 2018-10-06 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0017_auto_20181006_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 25, 15, 5, 28, 727975), verbose_name="Date d'expiration"),
        ),
    ]
