# Generated by Django 2.1.1 on 2018-10-18 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0034_auto_20181018_0216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compte',
            name='numero_compte',
        ),
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 7, 15, 6, 8, 198771), verbose_name="Date d'expiration"),
        ),
    ]
