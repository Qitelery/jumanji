# Generated by Django 3.1.2 on 2020-11-30 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumanji', '0010_auto_20201129_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='skills',
            field=models.CharField(default=1, max_length=600),
            preserve_default=False,
        ),
    ]
