# Generated by Django 2.1.2 on 2019-01-31 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0084_trader_emplacement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(blank=True, null=True, verbose_name="Date d'expiration"),
        ),
    ]