# Generated by Django 4.2.7 on 2023-12-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_match_end_time_match_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='player_number',
            field=models.IntegerField(default=10, verbose_name='Numéro de joueur'),
            preserve_default=False,
        ),
    ]
