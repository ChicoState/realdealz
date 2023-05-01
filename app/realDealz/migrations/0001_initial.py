# Generated by Django 4.1.7 on 2023-05-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('G', models.CharField(default='Action', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('P', models.CharField(default='PC', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sources', models.URLField(default='https://www.google.com/')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('appid', models.IntegerField(help_text='Unique ID for this particular game', primary_key=True, serialize=False)),
                ('name', models.CharField(default='-1', help_text='Game title', max_length=100)),
                ('price', models.FloatField(default='-1')),
                ('discount', models.CharField(default='-1', max_length=20)),
                ('developer', models.CharField(default='Unknown', max_length=100)),
                ('publisher', models.CharField(default='Unknown', max_length=100)),
                ('positive', models.CharField(default='-1', max_length=100)),
                ('negative', models.CharField(default='-1', max_length=100)),
                ('average_forever', models.CharField(default='-1', max_length=100)),
                ('average_2weeks', models.CharField(default='-1', max_length=100)),
                ('cover', models.ImageField(default='images/default.png', upload_to='images/')),
                ('genre', models.ManyToManyField(default='-1', help_text='Select Game genres', to='realDealz.genre')),
                ('platform', models.ManyToManyField(default='PC', help_text='Select Game platforms', to='realDealz.platform')),
            ],
        ),
    ]
