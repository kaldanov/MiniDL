# Generated by Django 2.2.7 on 2019-11-17 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0005_auto_20191117_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='group_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dl.Teacher'),
        ),
    ]
