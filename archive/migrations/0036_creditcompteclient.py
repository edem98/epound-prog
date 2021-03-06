# Generated by Django 2.1.2 on 2020-08-10 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0035_auto_20200715_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCompteClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_reference', models.CharField(max_length=255, null=True, unique=True, verbose_name='Identifiant Unique générée')),
                ('identifier', models.CharField(max_length=255, null=True, unique=True, verbose_name='Identifiant interne de la transaction de l’e-commerce')),
                ('payment_reference', models.CharField(max_length=255, null=True, verbose_name='Code de référence de paiement généré par Flooz')),
                ('amount', models.PositiveIntegerField(verbose_name='Montant payé par le client')),
                ('epound_transferer', models.PositiveIntegerField(null=True, verbose_name='Montant payé par le client')),
                ('datetime', models.DateTimeField(null=True)),
                ('payment_method', models.CharField(max_length=10, null=True, verbose_name='Méthode de paiement utilisée par le client')),
                ('phone_number', models.CharField(max_length=15, null=True, verbose_name='Numéro de téléphone du client')),
            ],
        ),
    ]
