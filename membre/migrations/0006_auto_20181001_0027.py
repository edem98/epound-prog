# Generated by Django 2.1.1 on 2018-10-01 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0005_auto_20180930_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprisecommerciale',
            name='compte_entreprise_commercial',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compteEntreprise_vers_entreprise', to='compte.CompteEntrepriseCommerciale', verbose_name='Compte e-B'),
        ),
    ]
