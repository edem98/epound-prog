# Generated by Django 2.1.2 on 2019-01-19 13:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0048_auto_20190118_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 8, 13, 19, 11, 29750), verbose_name="Date d'expiration"),
        ),
    ]