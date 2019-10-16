# Generated by Django 2.1.1 on 2018-10-27 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0049_auto_20181027_1653'),
        ('dashboard', '0007_auto_20181027_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remboursement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant_emprunter', models.PositiveIntegerField(null=True, verbose_name='Montant emprunter')),
                ('credit_actuel', models.PositiveIntegerField(null=True, verbose_name='Crédit actuel')),
                ('montant_rembourser', models.PositiveIntegerField(null=True, verbose_name='Montant rembouser')),
                ('reste', models.PositiveIntegerField(null=True, verbose_name='Reste à payer')),
                ('date_remboursement', models.DateTimeField(auto_now_add=True, verbose_name='Date de remboursement')),
                ('entreprise', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.EntrepriseCommerciale', verbose_name='Entreprise')),
            ],
        ),
    ]
