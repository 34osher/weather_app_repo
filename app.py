from flask import Flask, render_template, request
import requests
from countryinfo import CountryInfo  # Import the CountryInfo class
import pycountry
from datetime import datetime
import json

app = Flask(__name__)

BASE_URL = "https://api.weatherbit.io/v2.0/forecast/daily"
# Replace with your Weatherbit API key
API_KEY = '82ea16c35a4c4648a87d76a7a1e4edc9'


def get_weather_api(city_name):
    url = f"{BASE_URL}?days=7&city={city_name}&key={API_KEY}"
    response = requests.get(url)

    # Check if the response status code indicates success (200)
    if response.status_code == 200:
        try:
            # Attempt to decode the JSON response
            return response.json()
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            print("Raw Response:", response.text)
            return None
    else:  # any else status_code
        print("API Request Failed. Status Code:", response.status_code)
        print("Response Content:", response.text)
        return None


def filter_data(data_api):
    if data_api is None:
        return None

    country = pycountry.countries.get(alpha_2=data_api['country_code'])  # alpha2 = 2Letters CountryCode
    country_name = country.name if country else data_api['country_code']  # Get Country name if pycountry found it

    weather_data = {
        'city_name': data_api['city_name'],
        'country_name': country_name,
        'data': []
    }

    icon_url = "https://cdn.weatherbit.io/static/img/icons/"

    for day in data_api['data']:
        result = {
            'days_of_week': datetime.strptime(day['valid_date'], '%Y-%m-%d').strftime('%A'),
            'valid_date': day['valid_date'],
            'day_temp': day['high_temp'],
            'night_temp': day['low_temp'],
            'humidity': day['rh'],
            'icon': icon_url + day['weather']['icon'] + ".png",
            'wind_spd': day['wind_spd']
        }
        weather_data['data'].append(result)

    return weather_data


@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    weather_data = None

    if request.method == 'POST':
        location = request.form['location']
        search_type = request.form.get('search_type')
        value_location = location
        if search_type == 'country':
            try:
                # Use the CountryInfo class to get capital city name
                value_location = CountryInfo(location).capital()

            except (ValueError, requests.exceptions.RequestException):
                error_message = "Error getting weather data. Please try again."
            except (KeyError, requests.exceptions.RequestException):
                error_message = "Please try again. Invalid country"
            except (TypeError, requests.exceptions.RequestException):
                error_message = "Please try again. Invalid country"

        api_weather_data = get_weather_api(value_location)
        weather_data = filter_data(api_weather_data)
        # improvement of the code
        if weather_data is None:
            error_message = "Error getting weather data. Please try again."

    return render_template('index.html', error_message=error_message, weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
