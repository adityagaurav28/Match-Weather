from django.shortcuts import render

from . import models

from . import tasks

# Create your views here.

def index(request):
    tasks.weatherAndScoreSummary()
    givenDates = models.Dates_Detail.objects.all()
    return render(request, 'mainapp/main.html', {
        'details': givenDates
    })

