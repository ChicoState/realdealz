# Generated by Django 4.1.7 on 2023-04-26 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realDealz', '0008_alter_game_gamesite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='gameSite',
        ),
    ]
