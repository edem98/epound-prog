# Generated by Django 2.1.2 on 2018-11-09 18:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0055_auto_20181101_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='entreprisecommerciale',
            name='slug',
            field=models.SlugField(max_length=80, null=True, verbose_name='Etiquette'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 29, 18, 12, 6, 181753), verbose_name="Date d'expiration"),
        ),
    ]
