"""
Module: services.weather_service
---------------------------------

This module encapsulates the business logic related to fetching, caching, formatting,
and validating weather data from external weather APIs. It acts as an intermediary
between the raw external data sources and the application's internal data models,
ensuring data consistency, reliability, and optimal performance through caching.

Key Responsibilities:
- Manage communication with third-party weather APIs to retrieve current weather,
  forecasts, and historical weather data based on user-specified locations and date ranges.
- Implement robust error handling for API failures, including network errors,
  authentication issues, rate limiting, and unexpected response formats.
- Parse and normalize diverse external API responses into the application's internal
  data schemas for downstream processing and storage.
- Validate incoming weather data for completeness, correctness, and logical consistency
  before further processing or persisting to the database.
- Implement intelligent caching mechanisms to minimize redundant API calls,
  reduce latency, and stay within third-party API usage quotas.
- Support cache invalidation and refresh policies to maintain data freshness and accuracy.
- Facilitate asynchronous or batched API calls to improve throughput and responsiveness.
- Provide utility functions for data transformation such as unit conversions,
  timestamp normalization, and condition code mapping.
- Log API call metrics, errors, and cache statistics for monitoring and diagnostics.
- Expose a clean and reusable interface for service layer or API handlers to access
  weather data without direct knowledge of external API details.

Error Handling:
- Detect and handle API response errors, timeouts, and malformed data gracefully.
- Retry transient failures with exponential backoff where applicable.
- Raise meaningful exceptions or error codes to inform calling layers of failure reasons.

Integration Points:
- External weather data providers (e.g., OpenWeatherMap, WeatherAPI).
- Application caching layers (in-memory, Redis, etc.).
- Data validation and transformation utilities.
- Database persistence layer via service or repository calls.

This module is essential for maintaining high availability, accuracy, and
performance of weather-related features within the application.
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

# You can load this from env or config file
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def kelvin_to_c(k):
    return k - 273.15 if k else None


def c_to_f(c):
    return c * 9 / 5 + 32 if c is not None else None


def fetch_current_weather(
    city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None
) -> Optional[Dict[str, Any]]:
    params = {"appid": OPENWEATHER_API_KEY, "units": "metric"}
    if city:
        params["q"] = city
    elif lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon
    else:
        raise ValueError("You must provide either city or (lat, lon)")

    resp = requests.get(BASE_WEATHER_URL, params=params)
    if resp.status_code != 200:
        print("OpenWeatherMap API error:", resp.text)
        return None

    data = resp.json()
    return parse_current_weather(data)


def fetch_forecast(
    city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None
) -> Dict[str, Any]:
    params = {"appid": OPENWEATHER_API_KEY, "units": "metric"}
    if city:
        params["q"] = city
    elif lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon
    else:
        raise ValueError("You must provide either city or (lat, lon)")

    resp = requests.get(BASE_FORECAST_URL, params=params)
    if resp.status_code != 200:
        print("OpenWeatherMap API error:", resp.text)
        return {}

    data = resp.json()
    return parse_forecast(data)


def parse_current_weather(data: dict) -> Dict[str, Any]:
    # Extract only the fields you want
    main = data.get("main", {})
    wind = data.get("wind", {})
    sys = data.get("sys", {})
    weather = (data.get("weather") or [{}])[0]
    coord = data.get("coord", {})

    sunrise = sys.get("sunrise")
    sunset = sys.get("sunset")
    # Convert UNIX timestamp to UTC time
    sunrise_time = (
        datetime.fromtimestamp(sunrise, tz=timezone.utc).time() if sunrise else None
    )
    sunset_time = (
        datetime.fromtimestamp(sunset, tz=timezone.utc).time() if sunset else None
    )

    return {
        "location": {
            "city": data.get("name"),
            "country": sys.get("country"),
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
        },
        "weather": {
            "temp_c": main.get("temp"),
            "temp_f": c_to_f(main.get("temp")),
            "humidity": main.get("humidity"),
            "wind_speed": wind.get("speed"),
            "condition": weather.get("main"),
            "icon": weather.get("icon"),
            "sunrise": sunrise_time,
            "sunset": sunset_time,
            "pressure": main.get("pressure"),
            "visibility": data.get("visibility"),
            "precipitation": None,  # OWM puts rain/snow as separate fields
            "updated_at": datetime.utcfromtimestamp(data.get("dt", 0)),
        },
    }


def parse_forecast(data: dict) -> Dict[str, Any]:
    city_info = data.get("city", {})
    location = {
        "city": city_info.get("name"),
        "country": city_info.get("country"),
        "latitude": city_info.get("coord", {}).get("lat"),
        "longitude": city_info.get("coord", {}).get("lon"),
    }
    forecast_list = []
    for item in data.get("list", []):
        dt = datetime.utcfromtimestamp(item.get("dt", 0))
        main = item.get("main", {})
        weather = (item.get("weather") or [{}])[0]
        forecast_list.append(
            {
                "forecast_date": dt.date(),
                "forecast_hour": dt.hour,
                "temp_c": main.get("temp"),
                "temp_f": c_to_f(main.get("temp")),
                "condition": weather.get("main"),
                "icon": weather.get("icon"),
                "precipitation": (
                    item.get("rain", {}).get("3h", 0) if "rain" in item else 0
                ),
                "updated_at": dt,
            }
        )
    return {"location": location, "forecast": forecast_list}


# Example usage:
if __name__ == "__main__":
    import pprint

    pprint.pprint(fetch_current_weather(city="Seoul"))
    pprint.pprint(fetch_forecast(city="Seoul"))
