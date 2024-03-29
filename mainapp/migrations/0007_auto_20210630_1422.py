# Generated by Django 3.2.4 on 2021-06-30 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_match_detail_seriesid'),
    ]

    operations = [
        migrations.AddField(
            model_name='match_detail',
            name='matchEpochTime',
            field=models.IntegerField(default=100000001),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match_detail',
            name='matchLocalTime',
            field=models.TimeField(default='18:30:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match_detail',
            name='matchLocation',
            field=models.CharField(default='Not Provided', max_length=200),
            preserve_default=False,
        ),
    ]
