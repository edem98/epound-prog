# Generated by Django 2.1.1 on 2018-10-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_spécificationbesoin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expressionbesoin',
            options={'verbose_name': 'Besoins Humains'},
        ),
        migrations.AlterField(
            model_name='spécificationbesoin',
            name='image_illustratif',
            field=models.ImageField(blank=True, null=True, upload_to='specifications_besoins/', verbose_name='image associé'),
        ),
    ]
