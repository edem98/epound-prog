# Generated by Django 2.1.1 on 2018-10-25 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0044_auto_20181024_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 14, 14, 31, 28, 775487), verbose_name="Date d'expiration"),
        ),
    ]
