# Generated by Django 2.1.2 on 2019-01-25 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compte', '0050_auto_20190121_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='date_expiration',
            field=models.DateTimeField(verbose_name="Date d'expiration"),
        ),
    ]