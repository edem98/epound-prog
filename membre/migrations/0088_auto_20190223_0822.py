# Generated by Django 2.1.2 on 2019-02-23 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0087_membre_date_desactivation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='date_desactivation',
            field=models.DateField(blank=True, null=True, verbose_name='Date de desactivation'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateField(blank=True, null=True, verbose_name="Date d'expiration"),
        ),
    ]