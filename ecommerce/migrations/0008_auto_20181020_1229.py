# Generated by Django 2.1.1 on 2018-10-20 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_auto_20181020_1159'),
    ]

    operations = [
       
        migrations.RemoveField(
            model_name='productitem',
            name='vendeur',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductItem',
        ),
    ]
