# Generated by Django 3.0.5 on 2020-05-26 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listelement', '0001_initial'),
        ('comment', '0006_contact_type_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='element',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listelement.Element'),
        ),
    ]
