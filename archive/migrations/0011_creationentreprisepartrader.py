# Generated by Django 2.1.1 on 2018-10-18 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0038_auto_20181018_1459'),
        ('archive', '0010_auto_20181018_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreationEntrepriseParTrader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_trader', models.PositiveIntegerField(null=True, verbose_name='Code du Trader')),
                ('telephone', models.CharField(max_length=8, null=True, verbose_name='Téléphone du client')),
                ('mdp', models.CharField(max_length=50, null=True, verbose_name='Mot de passe')),
                ('consommateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.ConsommateurEntreprise')),
                ('trader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.Trader')),
            ],
        ),
    ]
