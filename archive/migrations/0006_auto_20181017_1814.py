# Generated by Django 2.1.1 on 2018-10-17 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0005_auto_20180128_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversiontrader',
            name='receveur_code',
            field=models.PositiveIntegerField(null=True, verbose_name='Code membre du Consommateur'),
        ),
        migrations.AddField(
            model_name='conversiontrader',
            name='trader_code',
            field=models.PositiveIntegerField(null=True, verbose_name='Code membre du Trader'),
        ),
        migrations.AddField(
            model_name='reconversiontrader',
            name='receveur_code',
            field=models.PositiveIntegerField(null=True, verbose_name='Code membre du Consommateur'),
        ),
        migrations.AddField(
            model_name='reconversiontrader',
            name='trader_code',
            field=models.PositiveIntegerField(null=True, verbose_name='Code membre du Trader'),
        ),
    ]
