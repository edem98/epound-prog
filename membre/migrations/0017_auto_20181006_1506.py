# Generated by Django 2.1.1 on 2018-10-06 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0016_auto_20181006_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='code_membre',
            field=models.PositiveIntegerField(unique=True, verbose_name='Code membre'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 25, 15, 5, 28, 827770), verbose_name="Date d'expiration"),
        ),
        migrations.AlterField(
            model_name='membre',
            name='mdp',
            field=models.CharField(max_length=80, verbose_name='Mot de passe'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='telephone',
            field=models.CharField(default=0, max_length=8, verbose_name='Téléphone'),
            preserve_default=False,
        ),
    ]
