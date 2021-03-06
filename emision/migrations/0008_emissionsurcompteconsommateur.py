# Generated by Django 2.1.1 on 2018-10-25 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0046_auto_20181025_1540'),
        ('emision', '0007_auto_20181025_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionSurCompteConsommateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.PositiveIntegerField(verbose_name='Montant Emit')),
                ('bonification', models.PositiveIntegerField(editable=False, verbose_name='Bonnification')),
                ('password', models.CharField(max_length=100, verbose_name='Confirmez votre mot de passe')),
                ('date_emission', models.DateTimeField(auto_now_add=True)),
                ('consommateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.Consommateur', verbose_name='Consommateur')),
                ('trader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.Trader', verbose_name='Trader')),
            ],
        ),
    ]
