# Generated by Django 2.1.1 on 2018-10-20 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0040_auto_20181019_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 12, 34, 2, 422499), verbose_name="Date d'expiration"),
        ),
    ]
