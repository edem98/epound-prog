# Generated by Django 2.1.2 on 2019-02-23 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0086_auto_20190204_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='membre',
            name='date_desactivation',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date de desactivation'),
        ),
    ]