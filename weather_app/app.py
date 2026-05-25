from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API Key - Get free key at https://openweathermap.org/api
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
BASE_URL = 'https://api.openweathermap.org/data/2.5'

def get_weather_data(city):
    """Fetch current weather data"""
    try:
        url = f'{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f'Error fetching weather: {str(e)}'}

def get_forecast_data(city):
    """Fetch 5-day forecast data"""
    try:
        url = f'{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Group forecast by day
        daily_forecasts = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = item
        
        return {'forecasts': list(daily_forecasts.values())[:5], 'city': data['city']['name']}
    except requests.exceptions.RequestException as e:
        return {'error': f'Error fetching forecast: {str(e)}'}

def format_weather_data(current_data):
    """Format weather data for display"""
    if 'error' in current_data:
        return current_data
    
    return {
        'city': current_data.get('name'),
        'country': current_data.get('sys', {}).get('country'),
        'temperature': round(current_data.get('main', {}).get('temp', 0)),
        'feels_like': round(current_data.get('main', {}).get('feels_like', 0)),
        'humidity': current_data.get('main', {}).get('humidity'),
        'pressure': current_data.get('main', {}).get('pressure'),
        'description': current_data.get('weather', [{}])[0].get('main', ''),
        'icon': current_data.get('weather', [{}])[0].get('icon', ''),
        'wind_speed': round(current_data.get('wind', {}).get('speed', 0), 1),
        'cloudiness': current_data.get('clouds', {}).get('all', 0),
        'sunrise': datetime.fromtimestamp(current_data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M'),
        'sunset': datetime.fromtimestamp(current_data.get('sys', {}).get('sunset', 0)).strftime('%H:%M'),
    }

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    """Get weather for requested city"""
    city = request.form.get('city', '').strip()
    
    if not city:
        return jsonify({'error': 'Please enter a city name'})
    
    if len(API_KEY) < 20 or API_KEY == 'your_api_key_here':
        return jsonify({'error': 'API key not configured. Please set OPENWEATHER_API_KEY environment variable.'})
    
    # Get current weather
    current_data = get_weather_data(city)
    
    if 'error' in current_data:
        return jsonify(current_data)
    
    current_weather = format_weather_data(current_data)
    
    # Get forecast
    forecast_data = get_forecast_data(city)
    
    return render_template('weather.html', 
                         weather=current_weather,
                         forecast=forecast_data.get('forecasts', []))

@app.route('/api/weather/<city>')
def api_weather(city):
    """API endpoint for weather data"""
    current_data = get_weather_data(city)
    forecast_data = get_forecast_data(city)
    
    if 'error' in current_data:
        return jsonify(current_data), 404
    
    return jsonify({
        'current': format_weather_data(current_data),
        'forecast': forecast_data.get('forecasts', [])
    })

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║        Weather App Running on http://localhost:5000   ║
    ║                                                        ║
    ║  To get started:                                      ║
    ║  1. Get free API key: https://openweathermap.org     ║
    ║  2. Set OPENWEATHER_API_KEY environment variable     ║
    ║  3. Or update 'your_api_key_here' in app.py          ║
    ╚════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
