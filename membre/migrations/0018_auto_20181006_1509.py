# Generated by Django 2.1.1 on 2018-10-06 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0017_auto_20181006_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='code_membre',
            field=models.PositiveIntegerField(null=True, unique=True, verbose_name='Code membre'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 25, 15, 9, 7, 475825), verbose_name="Date d'expiration"),
        ),
        migrations.AlterField(
            model_name='membre',
            name='mdp',
            field=models.CharField(max_length=80, null=True, verbose_name='Mot de passe'),
        ),
    ]
