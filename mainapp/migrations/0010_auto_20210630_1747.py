# Generated by Django 3.2.4 on 2021-06-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_series_detail_dateid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match_detail',
            name='matchDate',
        ),
        migrations.AddField(
            model_name='match_detail',
            name='matchLink',
            field=models.CharField(default='Null', max_length=500),
            preserve_default=False,
        ),
    ]
