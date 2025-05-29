"""
Module: services.weather_service
---------------------------------

This module encapsulates the business logic related to fetching, caching, formatting,
and validating weather data from external weather APIs. It acts as an intermediary
between the raw external data sources and the application's internal data models,
ensuring data consistency, reliability, and optimal performance through caching.

Key Responsibilities:
- Manage communication with third-party weather APIs to retrieve current weather,
  forecasts, and historical weather data based on user-specified locations
  and date ranges.
- Implement robust error handling for API failures, including network errors,
  authentication issues, rate limiting, and unexpected response formats.
- Parse and normalize diverse external API responses into the application's internal
  data schemas for downstream processing and storage.
- Validate incoming weather data for completeness, correctness, and logical consistency
  before further processing or persisting to the database.
- Implement intelligent caching mechanisms to minimize redundant API calls,
  reduce latency, and stay within third-party API usage quotas.
- Support cache invalidation & refresh policies to maintain data freshness and accuracy.
- Facilitate asynchronous or batched API calls to improve throughput and responsiveness.
- Provide utility functions for data transformation such as unit conversions,
  timestamp normalization, and condition code mapping.
- Log API call metrics, errors, and cache statistics for monitoring and diagnostics.
- Expose a clean and reusable interface for service layer or API handlers to access
  weather data without direct knowledge of external API details.

Error Handling:
- Detect and handle API response errors, timeouts, and malformed data gracefully.
- Retry transient failures with exponential backoff where applicable.
- Raise meaningful exceptions or error codes to inform calling layers of
  failure reasons.

Integration Points:
- External weather data providers (e.g., OpenWeatherMap, WeatherAPI).
- Application caching layers (in-memory, Redis, etc.).
- Data validation and transformation utilities.
- Database persistence layer via service or repository calls.

This module is essential for maintaining high availability, accuracy, and
performance of weather-related features within the application.
"""

import asyncio
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException
from rapidfuzz import process

from app.schemas.weather import (
    ForecastItem,
    ForecastResponse,
    WeatherBase,
    WeatherCurrent,
)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

KNOWN_CITIES = ["Seoul", "Busan", "New York", "Tokyo"]


def normalize_city_name(query: str) -> str:
    match, score, _ = process.extractOne(query, KNOWN_CITIES)
    return match if score > 80 else query


def get_weather_tip(condition: str) -> str:
    tip_map = {
        "Rain": "Bring an umbrella ☔️",
        "Snow": "Wear warm clothes ❄️",
        "Clear": "Perfect day for a walk 🌞",
        "Clouds": "Might be gloomy, stay productive ☁️",
        "Thunderstorm": "Stay indoors and safe ⛈️",
    }
    return tip_map.get(condition, "Stay prepared and check the forecast!")


def icon_url(icon_code: str) -> str:
    return f"/static/icons/{icon_code}.svg"


def c_to_f(c: Optional[float]) -> Optional[float]:
    if c is None:
        return None
    return c * 9 / 5 + 32


_cache: Dict[str, Dict[str, Any]] = {}


async def fetch_url(url: str, params: dict) -> Optional[dict]:
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail="API call failed"
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="External API request failed")


def _build_cache_key(prefix: str, **kwargs) -> str:
    return prefix + ":" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))


async def fetch_current_weather(
    city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None
) -> Optional[WeatherCurrent]:
    if not (city or (lat is not None and lon is not None)):
        raise ValueError("You must provide either city or (lat, lon)")

    params = {"appid": OPENWEATHER_API_KEY, "units": "metric"}
    if city:
        params["q"] = normalize_city_name(city)
    else:
        params["lat"] = lat
        params["lon"] = lon

    cache_key = _build_cache_key("current", **params)
    cached = _cache.get(cache_key)
    if cached and datetime.utcnow() - cached["timestamp"] < timedelta(minutes=10):
        return cached["data"]

    data = await fetch_url(BASE_WEATHER_URL, params)
    if not data:
        return None

    main = data.get("main", {})
    wind = data.get("wind", {})
    sys = data.get("sys", {})
    weather = (data.get("weather") or [{}])[0]

    sunrise = sys.get("sunrise")
    sunset = sys.get("sunset")

    result = WeatherCurrent(
        temp_c=main.get("temp", 0.0),
        temp_f=c_to_f(main.get("temp")) or 0.0,
        humidity=main.get("humidity", 0.0),
        wind_speed=wind.get("speed", 0.0),
        wind_deg=wind.get("deg"),
        wind_gust=wind.get("gust"),
        condition=weather.get("main", "Unknown"),
        condition_desc=weather.get("description", ""),
        icon=weather.get("icon", ""),
        icon_url=icon_url(weather.get("icon", "")),
        sunrise=(
            datetime.fromtimestamp(sunrise, tz=timezone.utc)
            if sunrise is not None
            else None
        ),
        sunset=(
            datetime.fromtimestamp(sunset, tz=timezone.utc)
            if sunset is not None
            else None
        ),
        pressure=main.get("pressure"),
        visibility=data.get("visibility"),
        precipitation=None,
        precipitation_type=None,
        uvi=None,
        weather_code=weather.get("id"),
        updated_at=datetime.fromtimestamp(data.get("dt", 0), tz=timezone.utc),
    )
    _cache[cache_key] = {"timestamp": datetime.utcnow(), "data": result}
    return result


async def fetch_forecast(
    city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None
) -> Optional[ForecastResponse]:
    if not (city or (lat is not None and lon is not None)):
        raise ValueError("You must provide either city or (lat, lon)")

    params = {"appid": OPENWEATHER_API_KEY, "units": "metric"}
    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon

    cache_key = _build_cache_key("forecast", **params)
    cached = _cache.get(cache_key)
    if cached and datetime.utcnow() - cached["timestamp"] < timedelta(minutes=30):
        return cached["data"]

    data = await fetch_url(BASE_FORECAST_URL, params)
    if not data:
        return None

    city_info = data.get("city", {})
    coord = city_info.get("coord", {})

    forecast_list = []
    for item in data.get("list", []):
        dt = datetime.fromtimestamp(item.get("dt"), tz=timezone.utc)
        main = item.get("main", {})
        weather = (item.get("weather") or [{}])[0]

        forecast_item = ForecastItem(
            forecast_date=dt.date(),
            forecast_hour=dt.hour,
            temp_c=main.get("temp", 0.0),
            temp_f=c_to_f(main.get("temp")) or 0.0,
            condition=weather.get("main", "Unknown"),
            condition_desc=weather.get("description", ""),
            icon=weather.get("icon", ""),
            icon_url=icon_url(weather.get("icon", "")),
            precipitation=item.get("rain", {}).get("3h", 0) if "rain" in item else 0,
            precipitation_type="rain" if "rain" in item else None,
            updated_at=dt,
            uvi=None,
            pressure=main.get("pressure"),
            wind_speed=item.get("wind", {}).get("speed"),
            wind_deg=item.get("wind", {}).get("deg"),
            wind_gust=item.get("wind", {}).get("gust"),
            humidity=main.get("humidity"),
            visibility=item.get("visibility"),
            weather_code=weather.get("id"),
        )
        forecast_list.append(forecast_item)

    result = ForecastResponse(
        location=WeatherBase(
            city=city_info.get("name"),
            country=city_info.get("country"),
            latitude=coord.get("lat"),
            longitude=coord.get("lon"),
        ),
        forecast=forecast_list,
    )

    _cache[cache_key] = {"timestamp": datetime.utcnow(), "data": result}
    return result


if __name__ == "__main__":

    async def main():
        current = await fetch_current_weather(city="Seoul")
        print(current)
        forecast = await fetch_forecast(city="Seoul")
        print(forecast)

    asyncio.run(main())
