import requests

def fetch_weather_open_meteo(lat, lon, date): #date format is YYYY-MM-DD
    """Takes location using latitude and longitude , and the current date to 
        return a dictionary of average weather values for that day and location

    
    Args:
        lat: latitude (float)
        lon: longitude (float)
        data: current data (string)
    
    Returns:
        a dictionary of average temperature, humidity and windspeed for that day and location """
    
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date, # same day
        "end_date": date, # same day
        "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m",
        "timezone": "auto"
    }
    try:
        res = requests.get(url, params=params) # getting the respons from the API
        res.raise_for_status()
        data = res.json() #Converts the returned JSON file into a dictionary used in Python

        #Accessing data for each weather component
        temps = data["hourly"]["temperature_2m"] 
        hums = data["hourly"]["relative_humidity_2m"]
        winds = data["hourly"]["windspeed_10m"]

        #filter for any NONE values

        temps = [t for t in temps if t is not None]
        hums = [h for h in hums if h is not None]
        winds = [w for w in winds if w is not None]

        #Case where temps or hums or winds are empty lists (no data)

        if not temps or not hums or not winds:
            print(f"Insufficient weather data for {lat},{lon} on {date}")
            return None

        return {
            #returning averages for each weather component
            "temperature": sum(temps)/len(temps), 
            "humidity": sum(hums)/len(hums),
            "wind_speed": sum(winds)/len(winds)
        }
    except requests.RequestException as e:
        print(f"Network error fetching weather for {lat},{lon} on {date}: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected API response structure for {lat},{lon} on {date}: {e}")
        return None
    except Exception as e:
        print(f"Failed to fetch weather for {lat},{lon} on {date}: {e}")
        return None


