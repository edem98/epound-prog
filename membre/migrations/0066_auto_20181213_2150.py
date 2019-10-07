# Generated by Django 2.1.2 on 2018-12-13 21:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0065_auto_20181213_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='consommateur',
            name='sexe',
            field=models.CharField(choices=[('Féminin', 'Féminin'), ('Masculin', 'Masculin')], default='Féminin', max_length=50, null=True, verbose_name='Sexe'),
        ),
        migrations.AddField(
            model_name='consommateur',
            name='ville_residence',
            field=models.CharField(max_length=150, null=True, verbose_name='Prénoms'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 21, 50, 14, 698522), verbose_name="Date d'expiration"),
        ),
    ]
