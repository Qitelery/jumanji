# Generated by Django 3.0.4 on 2020-10-18 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jumanji', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='skills',
        ),
    ]
