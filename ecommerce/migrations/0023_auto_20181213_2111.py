# Generated by Django 2.1.2 on 2018-12-13 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0022_auto_20181118_0930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expressionbesoin',
            options={'verbose_name': 'Besoin Humain', 'verbose_name_plural': 'Besoins Humains'},
        ),
        migrations.AlterModelOptions(
            name='produit',
            options={'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='spécificationbesoin',
            options={'verbose_name': 'Spécifiaction de Besoin', 'verbose_name_plural': 'Spécifiactions de Besoins'},
        ),
    ]