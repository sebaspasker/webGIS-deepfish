# Generated by Django 4.0.3 on 2022-05-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgisapp', '0008_rename_travels_travel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fish_plate',
            name='Peso',
            field=models.FloatField(null=True),
        ),
    ]
