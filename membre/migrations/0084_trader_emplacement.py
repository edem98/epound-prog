# Generated by Django 2.1.2 on 2019-01-25 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0083_remove_trader_emplacement'),
    ]

    operations = [
        migrations.AddField(
            model_name='trader',
            name='emplacement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quartier_trader', to='membre.Quartier'),
        ),
    ]