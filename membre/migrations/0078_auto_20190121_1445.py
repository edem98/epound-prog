# Generated by Django 2.1.2 on 2019-01-21 14:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0077_auto_20190121_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consommateur',
            name='nationalite',
            field=models.CharField(blank=True, choices=[('TOGO', 'TOGO'), ('BENIN', 'BENIN'), ('GHANA', 'GHANA')], default='TOGO', max_length=50, null=True, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='consommateur',
            name='sexe',
            field=models.CharField(blank=True, choices=[('Féminin', 'Féminin'), ('Masculin', 'Masculin')], default='Féminin', max_length=50, null=True, verbose_name='Sexe'),
        ),
        migrations.AlterField(
            model_name='consommateur',
            name='ville_residence',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Ville de résidence'),
        ),
        migrations.AlterField(
            model_name='consommateurentreprise',
            name='capital_social',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Caplital sociale'),
        ),
        migrations.AlterField(
            model_name='consommateurentreprise',
            name='nif',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='NIF'),
        ),
        migrations.AlterField(
            model_name='consommateurentreprise',
            name='numero_compte_bancaire',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro de compte bancaire'),
        ),
        migrations.AlterField(
            model_name='consommateurentreprise',
            name='numero_rccm',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Numéro RCCM'),
        ),
        migrations.AlterField(
            model_name='consommateurentreprise',
            name='objet_social',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Objet sociale'),
        ),
        migrations.AlterField(
            model_name='consommateurentreprise',
            name='regime_fiscal',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Régime fiscal'),
        ),
        migrations.AlterField(
            model_name='consommateurparticulier',
            name='date_naissance',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='consommateurparticulier',
            name='formation',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Formation'),
        ),
        migrations.AlterField(
            model_name='consommateurparticulier',
            name='lieu_residence',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Lieu de résidence'),
        ),
        migrations.AlterField(
            model_name='consommateurparticulier',
            name='num_carte',
            field=models.CharField(max_length=12, null=True, unique=True, verbose_name="Numéro de carte d'indentité"),
        ),
        migrations.AlterField(
            model_name='consommateurparticulier',
            name='profession',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Profession'),
        ),
        migrations.AlterField(
            model_name='consommateurparticulier',
            name='situation_matrimoniale',
            field=models.CharField(blank=True, choices=[('Célibataire', 'Célibataire'), ('Marié', 'Marié')], default='Célibataire', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='membre',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 10, 14, 45, 32, 276521), verbose_name="Date d'expiration"),
        ),
        migrations.AlterField(
            model_name='trader',
            name='sexe',
            field=models.CharField(blank=True, choices=[('Féminin', 'Féminin'), ('Masculin', 'Masculin')], default='Féminin', max_length=50, null=True, verbose_name='Sexe'),
        ),
        migrations.AlterField(
            model_name='trader',
            name='ville_residence',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Ville de résidence'),
        ),
    ]