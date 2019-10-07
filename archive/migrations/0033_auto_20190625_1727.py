# Generated by Django 2.1.2 on 2019-06-25 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0092_auto_20190625_1727'),
        ('archive', '0032_auto_20190513_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionConsommateurCommercial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_envoyeur', models.CharField(max_length=8, null=True, verbose_name="Téléphone de l'envoyeur")),
                ('numero_receveur', models.CharField(max_length=8, null=True, verbose_name='Téléphone du receveur')),
                ('montant_envoyer', models.PositiveIntegerField(null=True, verbose_name='Montant transférer')),
                ('solde_apres_transaction', models.PositiveIntegerField(null=True, verbose_name='Solde après transaction')),
                ('date_transaction', models.DateTimeField(auto_now_add=True, verbose_name='Date de Transaction')),
                ('envoyeur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.Consommateur', verbose_name='Expéditeur')),
                ('receveur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receveur_commercial', to='membre.EntrepriseCommerciale', verbose_name='Entreprise bénéficiaire')),
            ],
            options={
                'verbose_name': 'Transaction consommateur vers vendeur',
                'verbose_name_plural': 'Transactions consommateurs vers vendeurs',
            },
        ),
        migrations.RemoveField(
            model_name='payementconsomateur',
            name='envoyeur',
        ),
        migrations.RemoveField(
            model_name='payementconsomateur',
            name='receveur',
        ),
        migrations.DeleteModel(
            name='PayementConsomateur',
        ),
    ]
