# Generated by Django 2.1.1 on 2018-10-05 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0011_auto_20181004_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='membre',
            name='telephone',
            field=models.CharField(max_length=8, null=True, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 24, 20, 1, 18, 284795), verbose_name="Date d'expiration"),
        ),
    ]
