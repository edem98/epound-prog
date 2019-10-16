# Generated by Django 2.1.2 on 2019-09-01 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0026_auto_20190729_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produittroc',
            name='disponible',
        ),
        migrations.AddField(
            model_name='produittroc',
            name='status',
            field=models.CharField(choices=[('EN VENTE', 'EN VENTE'), ('VENDU', 'VENDU'), ('RETIRER', 'RETIRER')], default='EN VENTE', max_length=150),
        ),
    ]
