# Generated by Django 2.0 on 2018-01-02 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
    ]
