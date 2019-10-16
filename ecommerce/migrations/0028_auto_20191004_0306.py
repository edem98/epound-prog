# Generated by Django 2.1.2 on 2019-10-04 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0027_auto_20190901_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorie',
            options={'ordering': ['nom_categorie'], 'verbose_name': 'Catégorie', 'verbose_name_plural': 'Catégories'},
        ),
        migrations.AddField(
            model_name='produittroc',
            name='dernier_produit_souhaite',
            field=models.CharField(max_length=255, null=True, verbose_name='Dernier Produit Souhaite'),
        ),
        migrations.AddField(
            model_name='produittroc',
            name='premier_produit_souhaite',
            field=models.CharField(max_length=255, null=True, verbose_name='Premier Produit Souhaite'),
        ),
        migrations.AddField(
            model_name='produittroc',
            name='second_produit_souhaite',
            field=models.CharField(max_length=255, null=True, verbose_name='Second Produit Souhaite'),
        ),
    ]
