# Generated by Django 2.0 on 2018-01-03 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_requirements'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Requirements',
            new_name='Requirement',
        ),
    ]
