# Generated by Django 3.2.4 on 2021-07-25 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_match_detail_matchchanceofrain'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match_detail',
            old_name='matchWeatherTime',
            new_name='matchTime',
        ),
    ]
