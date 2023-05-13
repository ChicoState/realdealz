# Generated by Django 4.1.7 on 2023-05-03 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realDealz', '0014_remove_game_genre_game_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='genre',
        ),
        migrations.AddField(
            model_name='game',
            name='genre',
            field=models.ManyToManyField(default='Unknown', help_text='Select Game genres', to='realDealz.genre'),
        ),
    ]
