# Generated by Django 2.1.1 on 2018-10-18 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0032_auto_20181018_0216'),
        ('archive', '0006_auto_20181017_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayementConsomateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('envoyeur_code', models.PositiveIntegerField(null=True, verbose_name="Code membre de l'envoyeur")),
                ('receveur_code', models.PositiveIntegerField(null=True, verbose_name='Code membre du bénéficiare')),
                ('montant_envoyer', models.PositiveIntegerField(null=True, verbose_name='Montant transférer')),
                ('solde_apres_transaction', models.PositiveIntegerField(null=True, verbose_name='Solde après transaction')),
                ('date_transaction', models.DateTimeField(auto_now_add=True, verbose_name='Date de Transaction')),
                ('envoyeur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.Consommateur', verbose_name='envoyeur_consommateur')),
                ('receveur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receveur_commercial', to='membre.EntrepriseCommerciale', verbose_name='Entreprise bénéficiaire')),
            ],
        ),
        migrations.AlterField(
            model_name='conversiontrader',
            name='epounds_transferer',
            field=models.PositiveIntegerField(null=True, verbose_name='epounds transférer au client'),
        ),
        migrations.AlterField(
            model_name='conversiontrader',
            name='montant_converti',
            field=models.PositiveIntegerField(null=True, verbose_name='Somme Converti'),
        ),
        migrations.AlterField(
            model_name='conversiontrader',
            name='solde_apres_conversion',
            field=models.PositiveIntegerField(null=True, verbose_name='Solde après Conversion'),
        ),
        migrations.AlterField(
            model_name='transactioncommercialcomsommateur',
            name='montant_envoyer',
            field=models.PositiveIntegerField(null=True, verbose_name='Montant transférer'),
        ),
        migrations.AlterField(
            model_name='transactionintercomsommateur',
            name='montant_envoyer',
            field=models.PositiveIntegerField(verbose_name='Montant transférer'),
        ),
    ]
