# Generated by Django 3.0.5 on 2020-06-17 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listelement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='price',
            field=models.DecimalField(decimal_places=2, default=6.1, max_digits=10),
        ),
    ]
