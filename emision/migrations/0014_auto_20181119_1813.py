# Generated by Django 2.1.2 on 2018-11-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emision', '0013_auto_20181027_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creationparticulierpartrader',
            name='code_trader',
        ),
        migrations.AddField(
            model_name='creationparticulierpartrader',
            name='numero_trader',
            field=models.CharField(max_length=8, null=True, verbose_name='Numero du Trader'),
        ),
    ]
