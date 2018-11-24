# Generated by Django 2.1.1 on 2018-10-27 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20181001_0137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creancetotal',
            options={'verbose_name': 'Creance dûe', 'verbose_name_plural': 'Creance dûe'},
        ),
        migrations.AddField(
            model_name='creancetotal',
            name='total_epounds_consommateur',
            field=models.PositiveIntegerField(default=0, verbose_name='Cumul du solde des comptes consommateurs'),
        ),
        migrations.AlterField(
            model_name='creancetotal',
            name='total_epounds',
            field=models.PositiveIntegerField(default=0, verbose_name='Cumul du solde des comptes vendeurs'),
        ),
    ]
