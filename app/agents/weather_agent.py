"""
Weather Agent - Provides weather-related tools
"""
import requests
from typing import Optional, Dict, Any
from app.tools.tool_decorator import tool
from app.core.config import Config

@tool("get_current_weather")
def get_current_weather(city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current weather for a city
    
    Args:
        city: Name of the city (e.g., "London")
        country_code: Optional country code (e.g., "UK")
    
    Returns:
        Dictionary containing weather information
    """
    try:
        # In a real implementation, you would use a weather API like OpenWeatherMap
        # For now, we'll use a mock response or a free API
        # You can replace this with actual API calls
        
        # Check if we have an API key in config
        api_key = Config.get("weather.api_key", None)
        
        if api_key:
            # Example using OpenWeatherMap API
            location = f"{city},{country_code}" if country_code else city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    "city": city,
                    "country": country_code,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "success": True
                }
            else:
                return {
                    "error": f"Weather API error: {data.get('message', 'Unknown error')}",
                    "success": False
                }
        else:
            # Mock response for demonstration
            return {
                "city": city,
                "country": country_code or "Unknown",
                "temperature": 22.5,
                "feels_like": 23.0,
                "humidity": 65,
                "description": "Partly cloudy",
                "wind_speed": 5.2,
                "note": "Using mock data. Add OpenWeatherMap API key to config.yaml",
                "success": True
            }
    except Exception as e:
        return {
            "error": f"Failed to fetch weather: {str(e)}",
            "success": False
        }

@tool("get_weather_forecast")
def get_weather_forecast(city: str, days: int = 3, country_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Get weather forecast for multiple days
    
    Args:
        city: Name of the city
        days: Number of days to forecast (1-5)
        country_code: Optional country code
    
    Returns:
        Dictionary containing forecast information
    """
    try:
        # This would typically use a weather API with forecast capability
        # For demonstration, we'll return mock data
        
        api_key = Config.get("weather.api_key", None)
        
        if api_key and days <= 5:
            # Example using OpenWeatherMap forecast API
            location = f"{city},{country_code}" if country_code else city
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric&cnt={days}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                forecasts = []
                for item in data.get("list", [])[:days]:
                    forecasts.append({
                        "date": item.get("dt_txt", ""),
                        "temp": item["main"]["temp"],
                        "feels_like": item["main"]["feels_like"],
                        "humidity": item["main"]["humidity"],
                        "description": item["weather"][0]["description"],
                        "wind_speed": item["wind"]["speed"]
                    })
                
                return {
                    "city": city,
                    "country": country_code,
                    "forecast_days": days,
                    "forecasts": forecasts,
                    "success": True
                }
            else:
                return {
                    "error": f"Weather API error: {data.get('message', 'Unknown error')}",
                    "success": False
                }
        else:
            # Mock response
            mock_forecasts = []
            for i in range(min(days, 5)):
                mock_forecasts.append({
                    "day": i + 1,
                    "temperature": 20 + i,
                    "description": ["Sunny", "Partly cloudy", "Rainy", "Cloudy", "Clear"][i % 5],
                    "humidity": 60 + i * 5,
                    "wind_speed": 3 + i
                })
            
            return {
                "city": city,
                "country": country_code or "Unknown",
                "forecast_days": min(days, 5),
                "forecasts": mock_forecasts,
                "note": "Using mock data. Add OpenWeatherMap API key to config.yaml for real forecasts",
                "success": True
            }
    except Exception as e:
        return {
            "error": f"Failed to fetch forecast: {str(e)}",
            "success": False
        }

@tool("weather_health_check")
def weather_health_check() -> Dict[str, Any]:
    """
    Check if weather services are working
    
    Returns:
        Health status of weather services
    """
    try:
        # Test with a simple API call or configuration check
        api_key = Config.get("weather.api_key", None)
        
        if api_key:
            # Try a simple request to verify API key
            test_url = f"http://api.openweathermap.org/data/2.5/weather?q=London,UK&appid={api_key}"
            response = requests.get(test_url, timeout=5)
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "api_configured": True,
                    "api_working": True,
                    "message": "Weather API is properly configured and responding"
                }
            else:
                return {
                    "status": "degraded",
                    "api_configured": True,
                    "api_working": False,
                    "message": f"Weather API configured but returned error: {response.status_code}"
                }
        else:
            return {
                "status": "limited",
                "api_configured": False,
                "api_working": False,
                "message": "Weather API not configured. Using mock data only."
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "api_configured": False,
            "api_working": False,
            "error": str(e)
        }
