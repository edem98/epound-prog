# Generated by Django 2.1.1 on 2018-10-06 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0020_auto_20181006_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 25, 15, 42, 38, 956869), verbose_name="Date d'expiration"),
        ),
    ]
