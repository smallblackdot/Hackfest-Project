#new file
from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)

#@app.route("/")
#def home():
#    return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    #cityname="Bellevue"
    city = None
    lat=None
    lon=None
    latlon=None
    if request.method == "POST":
        city = request.form.get("city")
        if city=="":
            city = "Portland"
        weather = get_weather_data(city)
        lat, lon = get_lat_lon(city)  # Fetch coordinates for the entered city
        latlon = format_coordinates(lat, lon)  # Format the coordinates
        #API_KEY = "42b5a62bbca5e066cb5df3c67bcab130"  # Replace with your API key
        #if city:
        #    weather = get_weather_data(city)
        #else:
        #    weather = get_weather_data("Portland")
    
    return render_template("index.html", weather=weather, city=city, latlon=latlon) #lat=lat, lon=lon)

def get_weather_data(city):
    API_KEY = "42b5a62bbca5e066cb5df3c67bcab130"  # Replace with your API key
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use metric for Celsius temperature
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_lat_lon(city):
    """Fetch latitude and longitude for a city from OpenWeatherMap Geocoding API."""
    API_KEY = "42b5a62bbca5e066cb5df3c67bcab130"  # Replace with your API key
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    
    if response.status_code == 200 and response.json():
        data = response.json()[0]  # Get first result
        return data["lat"], data["lon"]
    return None, None  # Return None if no data found

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def round_up2(n, decimals=0):
    n2 = n
    if n < 0.0:
        n2 = -n;
    n3 = round(n2, decimals)
    if n < 0.0:
        n3 = -n3;
    return n3

def round_away_from_zero0(n, decimals=2):
    multiplier = 10 ** decimals
    if n > 0:
        return (int(n * multiplier + 0.5)) / multiplier
    else:
        return (int(n * multiplier - 0.5)) / multiplier
    
def round_away_from_zero(n, decimals=2):
    multiplier = 10 ** decimals
    if n > 0:
        return round((n * multiplier + 0.5) / multiplier, multiplier)
    else:
        return round((n * multiplier -0.5) / multiplier, multiplier)
def round_up3(n, decimals=2):
    
    if n <0:
        n -= 0.005
    return round(n, decimals)
    
def format_coordinates(lat, lon):
    # Round to two decimal places
    print(f"b4 lat: {lat}, lon: {lon}")
    lat = round_up3(lat, 2) #round(lat, 2)
    lon = round_up3(lon, 2) #round(lon, 2)
    #lat = round_away_from_zero(lat, 2) #round(lat, 2)
    #lon = round_away_from_zero(lon, 2) #round(lon, 2)
 
    print(f"aftr lat: {lat}, lon: {lon}")
    
    # Replace decimal points with 'd' and negative sign with 'n'
    lat_str = str(f"{lat:.2f}").replace('.', 'd')
    lon_str = str(f"{lon:.2f}").replace('-', 'n').replace('.', 'd')
    
    # Concatenate formatted latitude and longitude
    return f"{lat_str}{lon_str}"

# Example usage
#latitude = 47.6144219
#longitude = -122.192337
#formatted_location = format_coordinates(latitude, longitude)
#print(formatted_location)  # Output: "47d61n122d19"


if __name__ == "__main__":
    app.run(debug=True)
