from django.shortcuts import render
from opencage.geocoder import OpenCageGeocode

import requests
import json
from bs4 import BeautifulSoup
import datetime

from . import models

from . import tasks

# Create your views here.

def index(request):
    tasks.fetchMatch()
    tasks.weatherAndScoreSummary()
    givenDates = models.Dates_Detail.objects.all()
    return render(request, 'mainapp/main.html', {
        'details': givenDates
    })

