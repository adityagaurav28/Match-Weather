# Generated by Django 3.2.4 on 2021-07-03 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_auto_20210703_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='match_detail',
            name='matchChanceofRain',
            field=models.IntegerField(default=0),
        ),
    ]
