# Generated by Django 4.2.7 on 2023-12-11 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_match_match_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
