# Generated by Django 3.2.13 on 2023-02-23 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realDealz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='genre',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='price',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
