# Live Project

## Introduction
For the last two weeks of my time at the tech academy, I worked with my peers in a team developing a full scale Django Web Application in Python. The existing project was a travel website and I was tasked with developing a new application for the site. I saw how a good developer works with what they have to make a quality product. I worked on a [full stack story](#Weather App) that I am very proud of and was abale to gain experience working on both the back end and the front end of an application. Over the two week sprint I also had the opportunity to work on some other project management and team programming [skills](#other-skills-learned) that have made me a better developer.

Below is a description of the story I worked on, along with code snippets and navigation links. Some of the full code files I worked on are in this repo.

## Weather App
This user story was to create a weather application that would display the weather forcast for the user specified location. I utilized two API's for this application: one to get the geographic coordinates of the location the user searched for, and one to get the weather data for that location. I took the JSON data and converted it to a dictionary data type and then constructed a new dictionary of the desired data.

  `     locationUrl = 'http://www.mapquestapi.com/geocoding/v1/address?key=lSZeD1zxGvMTiOp6hbMj2YFfGAbt612T&location={}&maxResults=1'
        city = request.POST.get('City_Name', None)
        endPointLocation = locationUrl.format(city)
        locationDataJson = requests.get(endPointLocation).text
        locationData = json.loads(locationDataJson)
        location = {
            'city' : locationData['results'][0]['locations'][0]['adminArea5'],
            'state' : locationData['results'][0]['locations'][0]['adminArea3'],
            'country' : locationData['results'][0]['locations'][0]['adminArea1'],
            'latitude' : locationData['results'][0]['locations'][0]['latLng']['lat'],
            'longitude' : locationData['results'][0]['locations'][0]['latLng']['lng'],
        }
        lat = location['latitude']
        lon = location['longitude']

Similarly, I created a dictionary of the desired data from the weather API JSON response, and passed the data to the template. The weather data sometimes contained alerts for severe weather conditions. I wanted to include the alert data in the data returned to the template only if alert data existed for a location. I used Try/Except error handling to make sure only data that actually existed was being passed to the template.
         
         try:
            alerts = {
                'alert' : weatherData['alerts'][0]['title'],
                'alert_desc' : weatherData['alerts'][0]['description'],
            }
        except:
            return render(request, 'WeatherApp/weather.html', {'iconPaths' : iconPaths, 'location' : location, 'weather' : weather,                     'weekdays' : weekdays})
        else:
            return render(request, 'WeatherApp/weather.html', {'alerts' : alerts, 'iconPaths' : iconPaths, 'location' : location,                       'weather' : weather, 'weekdays' : weekdays})
            
I wanted to display the day of the week for the current date as well as the next five days to go along with the weather forcast. I created a small for loop to get each desired weekday and constructed them into a dictionary.
            
        base = datetime.date.today()
                weekdays = []
                for x in range(0, 6):
                    weekdays.append(base + datetime.timedelta(days = x))
                    
Using  HTML, Django TEmplate Language, and CSS I displayed the weather data in user friendly and visually appealing way.

This project gave me valuable experience creating an application to meet the needs of a user story. I was able to find the best APIs for my needs and utilize them to access the required data. I gained practice taking data from the back end and displaying it appropriately for the user.
      

## Other Skills Learned
* Working with a group of developers to identify bugs to the improve usability of an application.
* Improving project flow by communicating about who needs to check out which files for their current story.
* Learning new efficiencies from other developers by observing their workflow and asking questions.  
* Practice with team programming/pair programming when one developer runs into a bug they cannot solve.
* Participating in daily Stand-Up's to update the Project Manager and peers on my work.
* Planning how to complete a User Story and implementing that plan to satify the Story requirements.
* Producing results by a specified deadline.
  
*Jump to: [Back End Stories](#back-end-stories), [Page Top](#live-project)*
