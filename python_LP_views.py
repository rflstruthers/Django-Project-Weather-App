from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import os
import json 
import requests 
import datetime

def weatherSearch(request):

    #If user typed in a city:
    if request.method == 'POST':

    #THIS SECTION GETS THE DATES OF THE WEEK
        #Gets todays date, iterates through dates for next 5 days and adds them all to a list 
        base = datetime.date.today()
        weekdays = []
        for x in range(0, 6):
            weekdays.append(base + datetime.timedelta(days = x))
    #END WEEKDAY SECTION

    #THIS SECTION GETS THE COORDINATES OF THE LOCATION THAT THE USER SEARCHED FOR

        #API for geolocation
        locationUrl = 'http://www.mapquestapi.com/geocoding/v1/address?key=lSZeD1zxGvMTiOp6hbMj2YFfGAbt612T&location={}&maxResults=1'
    
        #gets user input for city name from weather.html
        city = request.POST.get('City_Name', None)

        #Combines the url with the user input:
        endPointLocation = locationUrl.format(city)

        #Sends that url to location API and stores the JSON file it gets back in 'locationDataJson' variable
        locationDataJson = requests.get(endPointLocation).text

        # json.loads reads and converts JSON from "locationDataJson" to Dictionary data type and stores it in 'locationData' variable
        locationData = json.loads(locationDataJson)
        print("\nLocation JSON: \n>>>{}{}".format(locationData, '<<<'))

        #Constructing a Dictionary that will contain all the information needed from the location JSON response
        location = {
            'city' : locationData['results'][0]['locations'][0]['adminArea5'],
            'state' : locationData['results'][0]['locations'][0]['adminArea3'],
            'country' : locationData['results'][0]['locations'][0]['adminArea1'],
            'latitude' : locationData['results'][0]['locations'][0]['latLng']['lat'],
            'longitude' : locationData['results'][0]['locations'][0]['latLng']['lng'],
        }
        
        #Variables to store latitude and longitude
        lat = location['latitude']
        lon = location['longitude']
    #END LOCATION SECTION

    #THIS SECTION USES THE COORDINATES TO GET THE WEATHER DATA FOR THAT LOCATION

        #API for weather data
        weatherUrl = 'https://api.darksky.net/forecast/05fbea0d932716f9dd2626d34506a68e/{},{}?exclude=minutely,hourly'

        #Combines the url with the user input:
        endPointWeather = weatherUrl.format(lat,lon)

        #Sends that url to the provider and store the JSON file inside "weatherDataJson"
        weatherDataJson = requests.get(endPointWeather).text

        # json.loads reads and converts JSON from "weatherDataJson" to Dictionary data type and stores it in 'weatherData' variable
        weatherData = json.loads(weatherDataJson)
        print("\nWeather JSON: \n>>>{}{}".format(weatherData, '<<<'))

        #Constructing a Dictionary that will contain all the information needed from the weather JSON response
        #Multiply the precipitation data by 100 to give a %
        weather = {
            'current_temp' : weatherData['currently']['temperature'],
            'day1_temp_high' : weatherData['daily']['data'][0]['temperatureHigh'],
            'day1_temp_low' : weatherData['daily']['data'][0]['temperatureLow'],
            'day2_temp_high' : weatherData['daily']['data'][1]['temperatureHigh'],
            'day2_temp_low' : weatherData['daily']['data'][1]['temperatureLow'],
            'day3_temp_high' : weatherData['daily']['data'][2]['temperatureHigh'],
            'day3_temp_low' : weatherData['daily']['data'][2]['temperatureLow'],
            'day4_temp_high' : weatherData['daily']['data'][3]['temperatureHigh'],
            'day4_temp_low' : weatherData['daily']['data'][3]['temperatureLow'],
            'day5_temp_high' : weatherData['daily']['data'][4]['temperatureHigh'],
            'day5_temp_low' : weatherData['daily']['data'][4]['temperatureLow'],
            'current_description' : weatherData['currently']['summary'],
            'day1_description' : weatherData['daily']['data'][0]['summary'],
            'day2_description' : weatherData['daily']['data'][1]['summary'],
            'day3_description' : weatherData['daily']['data'][2]['summary'],
            'day4_description' : weatherData['daily']['data'][3]['summary'],
            'day5_description' : weatherData['daily']['data'][4]['summary'], 
            'current_precip' : (weatherData['currently']['precipProbability'])*100,
            'day1_precip' : (weatherData['daily']['data'][0]['precipProbability'])*100,
            'day2_precip' : (weatherData['daily']['data'][1]['precipProbability'])*100,
            'day3_precip' : (weatherData['daily']['data'][2]['precipProbability'])*100,
            'day4_precip' : (weatherData['daily']['data'][3]['precipProbability'])*100,
            'day5_precip' : (weatherData['daily']['data'][4]['precipProbability'])*100,
            'current_icon' : weatherData['currently']['icon'],
            'day1_icon' : weatherData['daily']['data'][0]['icon'],
            'day2_icon' : weatherData['daily']['data'][1]['icon'],
            'day3_icon' : weatherData['daily']['data'][2]['icon'],
            'day4_icon' : weatherData['daily']['data'][3]['icon'],
            'day5_icon' : weatherData['daily']['data'][4]['icon'],
        }

        #Makes a list of the icon file paths to be used in weather.html
        iconPaths = [
            "/static/images/WeatherApp/{}.png".format(weather['current_icon']),
            "/static/images/WeatherApp/{}.png".format(weather['day1_icon']),
            "/static/images/WeatherApp/{}.png".format(weather['day2_icon']),
            "/static/images/WeatherApp/{}.png".format(weather['day3_icon']),
            "/static/images/WeatherApp/{}.png".format(weather['day4_icon']),
            "/static/images/WeatherApp/{}.png".format(weather['day5_icon']),
        ]

        #If there are any alerts, make a dictionary of them and pass them to weather.html, otherwise don't
        #and pass through all other data
        try:
            alerts = {
                'alert' : weatherData['alerts'][0]['title'],
                'alert_desc' : weatherData['alerts'][0]['description'],
            }
        except:
            return render(request, 'WeatherApp/weather.html', {'iconPaths' : iconPaths, 'location' : location, 'weather' : weather, 'weekdays' : weekdays})
        
        else:
            return render(request, 'WeatherApp/weather.html', {'alerts' : alerts, 'iconPaths' : iconPaths, 'location' : location, 'weather' : weather, 'weekdays' : weekdays})
      
    #END WEATHER SECTION

    #When page is first loaded
    else:
        return render(request, 'WeatherApp/preceed_weather.html')