# Generated by Django 2.1.2 on 2019-01-11 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0069_auto_20190111_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprisecommerciale',
            name='nature_jurique',
            field=models.CharField(choices=[('SNC', 'SNC'), ('SCS', 'SCS'), ('SARL', 'SARL'), ('SARL', 'SARL'), ('SARL', 'SARL'), ('SARL', 'SARL')], default='SNC', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='membre',
            name='code_membre',
            field=models.CharField(max_length=50, null=True, verbose_name='Code membre'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 31, 13, 48, 27, 650474), verbose_name="Date d'expiration"),
        ),
    ]
