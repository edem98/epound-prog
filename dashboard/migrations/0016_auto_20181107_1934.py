# Generated by Django 2.1.2 on 2018-11-07 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20181105_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='consommationmensuelmoyenneconsommateur',
            name='mois',
            field=models.CharField(max_length=50, null=True, verbose_name='Mois'),
        ),
        migrations.AddField(
            model_name='consommationmensuelmoyenneconsommateuractuel',
            name='mois',
            field=models.CharField(max_length=50, null=True, verbose_name='Mois actuel'),
        ),
        migrations.AddField(
            model_name='consommationmensuelmoyennevendeur',
            name='mois',
            field=models.CharField(max_length=50, null=True, verbose_name='Mois'),
        ),
        migrations.AddField(
            model_name='consommationmensuelmoyennevendeuractuel',
            name='mois',
            field=models.CharField(max_length=50, null=True, verbose_name='Mois actuel'),
        ),
    ]
