# Generated by Django 2.2.7 on 2019-12-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0009_files_studproc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studproc',
            name='room',
            field=models.IntegerField(),
        ),
    ]
