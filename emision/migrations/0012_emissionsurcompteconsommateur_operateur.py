# Generated by Django 2.1.1 on 2018-10-27 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emision', '0011_remove_emissionsurcompteconsommateur_trader'),
    ]

    operations = [
        migrations.AddField(
            model_name='emissionsurcompteconsommateur',
            name='operateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Opérateur'),
        ),
    ]
