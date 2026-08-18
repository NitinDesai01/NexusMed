import logging
from config.config import Config

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        
    def get_weather(self, city):
        """Get weather information"""
        return {
            "city": city,
            "temperature": 25,
            "condition": "Sunny",
            "humidity": 60
        }
    
    def get_weather_forecast(self, city, days=5):
        """Get weather forecast"""
        return {
            "city": city,
            "forecast": [{"day": i, "temp": 25 + i} for i in range(days)]
        }
