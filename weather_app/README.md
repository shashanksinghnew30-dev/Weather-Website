# 🌦️ Weather Predictor App

A Flask-based web application that displays current weather and 5-day forecasts for any city using the OpenWeatherMap API.

## Features

- **Current Weather Display**: Temperature, humidity, wind speed, pressure, and more
- **5-Day Forecast**: Detailed weather predictions
- **Search by City Name**: Easy city lookup
- **Quick City Links**: Buttons for popular cities
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Data**: Uses OpenWeatherMap free API

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Navigate to the weather_app directory**:
   ```bash
   cd weather_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get API Key**:
   - Go to [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate a free API key (valid in 10 minutes)

4. **Configure API Key**:
   - Create a `.env` file (copy from `.env.example`):
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and replace `your_api_key_here` with your actual API key
   
   OR directly edit `app.py` line 13:
   ```python
   API_KEY = 'your_actual_api_key_here'
   ```

## Running the App

```bash
python app.py
```

The app will start on `http://localhost:5000`

### Access the App

- Open your browser and go to: **http://localhost:5000**
- Enter a city name to get weather information
- Use quick links for popular cities

## Project Structure

```
weather_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── README.md             # This file
├── templates/
│   ├── index.html        # Home page
│   └── weather.html      # Weather display page
└── static/
    └── style.css         # Styling
```

## API Endpoints

### GET `/`
Returns the home page with search form.

### POST `/weather`
Accepts form data with city name and returns weather page.
- **Parameters**: `city` (string)

### GET `/api/weather/<city>`
Returns JSON data for weather and forecast.
- **Response**: JSON with current weather and 5-day forecast

## Features Explained

### Current Weather
- Temperature (°C)
- "Feels like" temperature
- Weather description
- Humidity percentage
- Wind speed (m/s)
- Atmospheric pressure (hPa)
- Cloud coverage percentage
- Sunrise and sunset times

### 5-Day Forecast
- Daily temperature
- Weather conditions with icons
- Humidity and wind speed for each day

## Troubleshooting

### "API key not configured" Error
- Ensure you've set the `OPENWEATHER_API_KEY` environment variable
- Check that `.env` file exists with correct API key
- Restart the application after adding the API key

### "City not found" Error
- Double-check the spelling of the city name
- Try using the city's English name
- Some small towns may not be available in the API

### Connection Timeout
- Check your internet connection
- OpenWeatherMap API might be temporarily unavailable
- Try again in a few moments

## Free API Limits

The free tier of OpenWeatherMap includes:
- **Current weather**: No request limit
- **Forecasts**: Up to 5 days
- **Requests**: Up to 1,000 calls per day

## Customization

### Change Port
Edit `app.py` last line:
```python
app.run(debug=True, port=8000)  # Change 5000 to desired port
```

### Change Temperature Units
In `app.py`, modify the API calls from `units=metric` to `units=imperial` for Fahrenheit

### Add More Cities to Quick Links
Edit `templates/index.html` in the `quick-links` section

## License

Open source - feel free to modify and use!

## Next Steps

- Add location-based weather using geolocation
- Store search history
- Add weather alerts
- Create mobile app version
- Add more detailed charts and graphs
