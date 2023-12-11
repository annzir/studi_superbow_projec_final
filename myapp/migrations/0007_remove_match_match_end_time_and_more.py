# Generated by Django 4.2.7 on 2023-12-11 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_match_match_end_time_match_match_starting_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='match_end_time',
        ),
        migrations.RemoveField(
            model_name='match',
            name='match_starting_time',
        ),
        migrations.AddField(
            model_name='match',
            name='odds_team1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='odds_team2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
