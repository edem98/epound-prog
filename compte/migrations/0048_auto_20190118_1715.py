# Generated by Django 2.1.2 on 2019-01-18 17:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0047_auto_20181213_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='comptegrenier',
            name='montant_reconverti_local',
            field=models.PositiveIntegerField(null=True, verbose_name='cumul des 70% des reconversions vendeurs'),
        ),
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 7, 17, 15, 40, 435074), verbose_name="Date d'expiration"),
        ),
    ]