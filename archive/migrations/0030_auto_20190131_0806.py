# Generated by Django 2.1.2 on 2019-01-31 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0029_reconversiontrader_mdp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconversiontrader',
            name='solde_consommateur_apres_reconversion',
            field=models.PositiveIntegerField(null=True, verbose_name='Solde Trader après Reconversion'),
        ),
    ]