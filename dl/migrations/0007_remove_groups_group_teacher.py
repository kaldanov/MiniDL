# Generated by Django 2.2.7 on 2019-11-17 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0006_groups_group_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groups',
            name='group_teacher',
        ),
    ]
