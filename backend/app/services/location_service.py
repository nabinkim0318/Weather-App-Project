"""
Module: services.location_service
------------------------------

This module provides location search functionality, including geocoding services
for converting addresses, city names, and zip codes to coordinates.
"""

from typing import List, Optional

import httpx

from app.core.config import get_settings


async def search_location(query: str) -> List[dict]:
    """
    Search for locations using OpenWeatherMap Geocoding API.
    Returns a list of locations matching the query.
    """
    settings = get_settings()
    base_url = "http://api.openweathermap.org/geo/1.0/direct"

    # Check if query is a zip code (simple check for now)
    if query.replace("-", "").isdigit():
        base_url = "http://api.openweathermap.org/geo/1.0/zip"
        params = {"zip": query, "appid": settings.openweather_api_key}
    else:
        params = {"q": query, "limit": 5, "appid": settings.openweather_api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):  # Single location response (zip code)
                return [
                    {
                        "name": data.get("name", ""),
                        "lat": data.get("lat"),
                        "lon": data.get("lon"),
                        "country": data.get("country", ""),
                    }
                ]
            else:  # List of locations (city search)
                return [
                    {
                        "name": loc.get("name", ""),
                        "lat": loc.get("lat"),
                        "lon": loc.get("lon"),
                        "country": loc.get("country", ""),
                        "state": loc.get("state"),
                    }
                    for loc in data
                ]
    except Exception as e:
        print(f"Error searching location: {str(e)}")
        return []


async def get_location_by_coordinates(lat: float, lon: float) -> Optional[dict]:
    """
    Reverse geocoding: Get location information from coordinates
    """
    try:
        settings = get_settings()
        async with httpx.AsyncClient() as client:
            params = {
                "lat": lat,
                "lon": lon,
                "limit": 1,
                "appid": settings.openweather_api_key,
            }
            response = await client.get(
                "http://api.openweathermap.org/geo/1.0/reverse", params=params
            )
            response.raise_for_status()

            locations = response.json()
            if locations:
                loc = locations[0]
                return {
                    "name": loc.get("name"),
                    "country": loc.get("country"),
                    "state": loc.get("state"),
                    "lat": loc.get("lat"),
                    "lon": loc.get("lon"),
                }
            return None
    except Exception as e:
        print(f"Error getting location by coordinates: {e}")
        return None
