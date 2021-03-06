# Generated by Django 2.1.1 on 2018-10-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_auto_20181014_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionintercomsommateur',
            name='envoyeur_code',
            field=models.PositiveIntegerField(null=True, verbose_name="Code membre de l'envoyeur"),
        ),
        migrations.AddField(
            model_name='transactionintercomsommateur',
            name='receveur_code',
            field=models.PositiveIntegerField(null=True, verbose_name='Code membre du bénéficiare'),
        ),
    ]
