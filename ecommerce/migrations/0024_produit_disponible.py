# Generated by Django 2.1.2 on 2019-06-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0023_auto_20181213_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]