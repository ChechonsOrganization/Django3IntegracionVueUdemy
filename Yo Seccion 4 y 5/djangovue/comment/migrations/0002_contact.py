# Generated by Django 3.0.5 on 2020-05-19 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=70)),
                ('phone', models.CharField(max_length=13)),
                ('date_birth', models.DateField()),
                ('documento', models.FileField(upload_to='uploads/contact')),
            ],
        ),
    ]
