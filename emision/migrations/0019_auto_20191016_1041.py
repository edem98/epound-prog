# Generated by Django 2.1.2 on 2019-10-16 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emision', '0018_creationparticulierpartraderetintegrateur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creationparticulierpartraderetintegrateur',
            name='numero_integrateur',
            field=models.CharField(max_length=8, null=True, verbose_name="Numero de l'integrateur"),
        ),
    ]