# Generated by Django 3.1.2 on 2020-11-29 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jumanji', '0008_auto_20201108_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.CharField(max_length=5000),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=64)),
                ('salary', models.IntegerField()),
                ('qualification', models.CharField(max_length=64)),
                ('education', models.CharField(max_length=64)),
                ('experience', models.TextField(max_length=5000)),
                ('portfolio', models.CharField(max_length=64)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to='jumanji.specialty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]