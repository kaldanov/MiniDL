# Generated by Django 2.2.6 on 2019-11-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(to='dl.Courses'),
        ),
    ]
