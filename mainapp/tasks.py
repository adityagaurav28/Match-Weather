import requests
from bs4 import BeautifulSoup
import datetime

from requests.api import head

from . import models

from opencage.geocoder import OpenCageGeocode


def fetchCoordinates(address):
    key = '7c1323c1b53c48dd83ccd2dc9b93a8e0'
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(address)
    return results[0]['geometry']['lat'],results[0]['geometry']['lng']

def fetchMatch():
    lastUpdateTime = models.UpdateDataTime.objects.get(pk=1)
    print(lastUpdateTime.updatedRecently())
    currentTime = int(datetime.datetime.now().timestamp())    


    if lastUpdateTime.updatedRecently():
        models.Dates_Detail.objects.all().delete()
        url = 'https://www.cricbuzz.com/cricket-schedule/upcoming-series/all'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        dates = soup.findAll('div', attrs = {'class':'cb-col-100 cb-col'})
        count = 0
        for date in dates:
            dateElement = date.find('div', attrs = {'class':'cb-lv-grn-strip text-bold'})
            if dateElement is not None:
                count = count + 1
            else:
                continue
            serieses = date.findAll('div', attrs = {'class':'cb-col-100 cb-col'})
            for series in serieses:
                seriesName = series.find('a', attrs={'class':'cb-col-33 cb-col cb-mtchs-dy text-bold'})
                matches = series.find('div', attrs={'class':'cb-col-67 cb-col'})
                matchesInfo = matches.findAll('div', attrs={'class':'cb-ovr-flo cb-col-60 cb-col cb-mtchs-dy-vnu cb-adjst-lst'})
                matchesTime = matches.findAll('div',attrs={'class':'cb-col-40 cb-col cb-mtchs-dy-tm cb-adjst-lst'})
                for i in range(len(matchesInfo)):
                    match = matchesInfo[i].find('a', attrs={})
                    matchlink = "https://www.cricbuzz.com/api/html/cricket-hscorecard/" + match.get('href')[21:26]
                    time = matchesTime[i].findAll('span', attrs={'class':'schedule-date'})
                    epochTime = int(time[0].get('timestamp')[:-3])
                    localDateTime = datetime.datetime.fromtimestamp(epochTime)
                    address = matchesInfo[i].find('div', attrs={'itemprop':"location"})
                    stadiumName = address.find('span', attrs={'itemprop':"name"})
                    locality = address.find('span', attrs={'itemprop':"addressLocality"})
                    location = stadiumName.text + ' ' + locality.text

                    latitude, longitude = fetchCoordinates(location)

                    localDate = localDateTime.date()

                    dateModel, res = models.Dates_Detail.objects.get_or_create(onDate=localDate)
                    if res:
                        dateModel.save()
                    dateId = models.Dates_Detail.objects.get(onDate=localDate)

                    seriesModel, res = models.Series_Detail.objects.get_or_create(seriesName=seriesName.text,dateId=dateId)
                    if res:
                        seriesModel.save()                
                    seriesId = models.Series_Detail.objects.get(seriesName=seriesName.text,dateId=dateId)

                    test = models.Match_Detail(matchName=match.text,seriesId=seriesId,matchLocalTime=localDateTime.time(),matchEpochTime=epochTime,matchLocation=location,
                    matchLatitude = latitude, matchLongitude = longitude, matchLink = matchlink)

                    if currentTime < epochTime - 3600:
                        match.matchTime = 'future'
                        futureWeatherSummary(test)

                    test.save()    
            if count == 2:
                break
        lastUpdateTime.changeTime = datetime.datetime.now() + datetime.timedelta(hours=3)
        lastUpdateTime.save()

def fetchCurrentWeatherSummary(matchObject, currentTime):
    weatherURL = 'https://api.weatherapi.com/v1/forecast.json?key=bfc4226b16254458b9a120956212606&q={},{}&days=1&aqi=no&alerts=no'.format(matchObject.matchLatitude,matchObject.matchLongitude)
    response = requests.get(weatherURL).json()
    currentWeather = response['current']
    matchObject.matchTemp = currentWeather['temp_c']    
    matchObject.matchCloud = currentWeather['cloud']  
    matchObject.matchHumidity = currentWeather['humidity']   
    matchObject.matchCondition = currentWeather['condition'] 
    dayForecast = response['forecast']['forecastday'][0]['hour']
    for hourForecast in dayForecast:
        if (currentTime -3600) <= hourForecast['time_epoch'] <= currentTime:
            matchObject.matchChanceofRain = hourForecast['chance_of_rain']
            break


def futureHour(dayForecast,matchObject):
    for hourObject in dayForecast:
        if hourObject['time_epoch'] >= matchObject.matchEpochTime - 1800:
            currentWeather = hourObject
            matchObject.matchTemp = currentWeather['temp_c']    
            matchObject.matchCloud = currentWeather['cloud']  
            matchObject.matchHumidity = currentWeather['humidity']   
            matchObject.matchCondition = currentWeather['condition']  
            matchObject.matchChanceofRain = currentWeather['chance_of_rain']  
            break


def futureWeatherSummary(matchObject):
    lastUpdateTime = models.UpdateDataTime.objects.get(pk=1)
    if lastUpdateTime.updatedRecently():
        weatherURL = 'https://api.weatherapi.com/v1/forecast.json?key=bfc4226b16254458b9a120956212606&q={},{}&days=3&aqi=no&alerts=no'.format(matchObject.matchLatitude,matchObject.matchLongitude)
        response = requests.get(weatherURL).json()
        forecastAllDays = response['forecast']['forecastday']
        if forecastAllDays[0]['date_epoch'] <= matchObject.matchEpochTime <= forecastAllDays[1]['date_epoch']:
            futureHour(forecastAllDays[0]['hour'],matchObject)
        elif forecastAllDays[1]['date_epoch'] <= matchObject.matchEpochTime <= forecastAllDays[2]['date_epoch']:
            futureHour(forecastAllDays[1]['hour'],matchObject)
            

def fetchScoreTeams(matchObject, soup):    
    headings = soup.findAll('div', attrs = {'class':'cb-col cb-col-100 cb-scrd-hdr-rw'})
    headings = headings[:-1]
    if len(headings) == 1:
        matchObject.matchFirstInning = headings[0].text.strip()
    elif len(headings) == 2:
        matchObject.matchFirstInning = headings[0].text.strip()
        matchObject.matchSecondInning = headings[1].text.strip()
    

def fetchScoreSummary(matchObject):
    url = matchObject.matchLink
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    status = soup.find('div', attrs = {'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-preview'})
    if status is None:
        status = soup.find('div', attrs = {'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-complete'})
    if status is None:
        status = soup.find('div', attrs = {'class':'cb-col cb-scrcrd-status cb-col-100 cb-text-live'})
    if status is not None:
        fetchScoreTeams(matchObject, soup)
        matchObject.matchStatus = status.text
    

def weatherAndScoreSummary():
    matches = models.Match_Detail.objects.all()    
    currentTime = int(datetime.datetime.now().timestamp())    
    for match in matches:
        if currentTime > match.matchEpochTime - 3600:
            match.matchTime = 'current'
            fetchScoreSummary(match)
            fetchCurrentWeatherSummary(match,currentTime)
        match.save()