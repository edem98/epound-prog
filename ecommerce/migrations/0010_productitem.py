# Generated by Django 2.1.1 on 2018-10-20 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0041_auto_20181020_1234'),
        ('ecommerce', '0009_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=50, null=True)),
                ('modele', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(null=True)),
                ('image_produit', models.ImageField(null=True, upload_to='produits/', verbose_name='Image')),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('produit_associer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Product')),
                ('vendeur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membre.EntrepriseCommerciale')),
            ],
        ),
    ]
