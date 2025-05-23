from django.shortcuts import render
import requests
import datetime


def index(request):
    api_key = '3ed65bca1b27653ff869625b305a8f48'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'

    # Define the background image map
    # Background image map - Ensure paths match existing image files in static/images/
    background_image_map = {
        'new york': '/static/images/new-york.jpg',
        'london': '/static/images/london.jpg',
        'paris': '/static/images/paris.jpg',
        'tokyo': '/static/images/tokyo.jpg',
        'sydney': '/static/images/sydney.jpeg',
        'beijing': '/static/images/beijing.jpeg',
        'moscow': '/static/images/moscow.jpeg',
        'rio de janeiro': '/static/images/rio-de-janeiro.jpeg',
        'mumbai': '/static/images/mumbai.jpeg',
        'shanghai': '/static/images/shanghai.jpeg',
        'bangkok': '/static/images/bangkok.jpeg',
        'cape town': '/static/images/cape-town.jpeg',
        'dubai': '/static/images/dubai.jpeg',
        'istanbul': '/static/images/istanbul.jpeg',
        'berlin': '/static/images/berlin.jpeg',
        'madrid': '/static/images/madrid.jpeg',
        'rome': '/static/images/rome.jpeg',
        'athens': '/static/images/athens.jpeg',
        'cairo': '/static/images/cairo.jpeg',
        'jakarta': '/static/images/jakarta.jpeg',
        'hong kong': '/static/images/hong-kong.jpeg',
        'seoul': '/static/images/seoul.jpeg',
        'vienna': '/static/images/vienna.jpeg',
        'oslo': '/static/images/oslo.jpeg',
        'stockholm': '/static/images/stockholm.jpeg',
        'helsinki': '/static/images/helsinki.jpeg',
        'lisbon': '/static/images/lisbon.jpeg',
        'warsaw': '/static/images/warsaw.jpeg',
        'prague': '/static/images/prague.jpeg',
        'zurich': '/static/images/zurich.jpeg',
        'brussels': '/static/images/brussels.jpeg',
        'amsterdam': '/static/images/amsterdam.jpeg',
        'buenos aires': '/static/images/buenos-aires.jpeg',
        'santiago': '/static/images/santiago.jpeg',
        'bogota': '/static/images/bogota.jpeg',
        'nairobi': '/static/images/nairobi.jpeg',
        'kuala lumpur': '/static/images/kuala-lumpur.jpeg',
        'singapore': '/static/images/singapore.jpeg',
        'manila': '/static/images/manila.jpeg',
        'hanoi': '/static/images/hanoi.jpeg',
        'melbourne': '/static/images/melbourne.jpeg',
        'perth': '/static/images/perth.jpeg',
        'auckland': '/static/images/auckland.jpeg',
        'doha': '/static/images/doha.jpeg',
        'riyadh': '/static/images/riyadh.jpeg',
        'johannesburg': '/static/images/johannesburg.jpeg',
        'lagos': '/static/images/lagos.jpeg',
        'venice': '/static/images/venice.jpeg',
    }

    # Set a default background image
    default_background_image = '/static/images/default-background.jpg'

    # Retrieve the background image based on the city
    city = request.POST.get('city', '').strip().lower() if request.method == 'POST' else 'default'
    background_image = background_image_map.get(city, default_background_image)

    if request.method == 'POST':
        if city:
            weather_data, daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)
            context = {
                'weather_data': weather_data,
                'daily_forecasts': daily_forecasts,
                'background_image': background_image,  # Set city-specific background
            }
        else:
            context = {
                'background_image': default_background_image,  # Default background if no city is provided
            }
    else:
        context = {
            'background_image': default_background_image,  # Default background
        }

    return render(request, 'weather_app/index.html', context)


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Get current weather
    response = requests.get(current_weather_url.format(city, api_key)).json()
    if response.get('cod') != 200:
        print(f"Error fetching weather data: {response.get('message')}")
        return None, None

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    # Get 5-day forecast
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()
    if forecast_response.get('cod') != "200":
        print(f"Error fetching forecast data: {forecast_response.get('message')}")
        return weather_data, None

    # Parse the forecast response
    daily_forecasts = []
    for i in range(0, len(forecast_response['list']), 8):  # 8 data points = 1 day (3-hour intervals)
        daily_data = forecast_response['list'][i]
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['main']['temp_min'] - 273.15, 2),
            'max_temp': round(daily_data['main']['temp_max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
