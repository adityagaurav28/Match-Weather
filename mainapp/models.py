from collections import defaultdict
import datetime
from django.db import models

from django.utils import timezone

# Create your models here.

class UpdateDataTime(models.Model):
    changeTime = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.changeTime}"

    def updatedRecently(self):
        return self.changeTime < timezone.now()

class Dates_Detail(models.Model):
    dateId = models.AutoField(primary_key=True)
    onDate = models.DateField()

    def __str__(self) -> str:
        return f"{self.dateId} {self.onDate}"

class Series_Detail(models.Model):
    seriesId = models.AutoField(primary_key=True)
    seriesName = models.CharField(max_length=100)
    dateId = models.ForeignKey(Dates_Detail,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.seriesId} {self.seriesName}"

class Match_Detail(models.Model):
    matchId = models.AutoField(primary_key=True)
    matchName = models.CharField(max_length=100)
    seriesId = models.ForeignKey(Series_Detail, db_column='seriesId', on_delete=models.CASCADE)
    matchLocalTime = models.TimeField()
    matchEpochTime = models.IntegerField()
    matchLocation = models.CharField(max_length=200)
    matchLatitude = models.FloatField(default=0)
    matchLongitude = models.FloatField(default=0)
    matchLink = models.CharField(max_length=500,default='NULL')
    matchTime = models.CharField(max_length=50,default='future')
    matchTemp = models.FloatField(default=30)
    matchCloud = models.IntegerField(default=0)
    matchHumidity = models.IntegerField(default=0)
    matchCondition = models.JSONField(default = dict)
    matchChanceofRain = models.IntegerField(default=0)
    matchStatus = models.CharField(max_length=500,default='Scores will appear once the match starts.')
    matchFirstInning = models.CharField(max_length=500, default='Not Started')
    matchSecondInning = models.CharField(max_length=500,default='Not Started')


    def __str__(self) -> str:
        return f"{self.matchId} {self.matchName}"