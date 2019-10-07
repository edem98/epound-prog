# Generated by Django 2.1.1 on 2018-10-17 23:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0030_auto_20181017_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 6, 23, 2, 55, 631531), verbose_name="Date d'expiration"),
        ),
        migrations.AlterField(
            model_name='comptebusiness',
            name='taux_contribution',
            field=models.DecimalField(decimal_places=1, default=0.05, editable=False, max_digits=2, verbose_name='Taux de contibution mensuel'),
        ),
        migrations.AlterField(
            model_name='comptebusiness',
            name='taux_reconversion',
            field=models.DecimalField(decimal_places=1, default=0.7, editable=False, max_digits=2, verbose_name='Taux de reconversion'),
        ),
        migrations.AlterField(
            model_name='compteconsommateur',
            name='taux_gain',
            field=models.DecimalField(decimal_places=1, default=1.5, editable=False, max_digits=2, verbose_name="Taux d'intérêt"),
        ),
        migrations.AlterField(
            model_name='compteconsommateur',
            name='taux_perte',
            field=models.DecimalField(decimal_places=1, default=0.6, editable=False, max_digits=2, verbose_name='Taux de reconversion'),
        ),
        migrations.AlterField(
            model_name='compteentreprisecommerciale',
            name='taux_rembourssement',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2, verbose_name="Taux d'intérêt"),
        ),
    ]
