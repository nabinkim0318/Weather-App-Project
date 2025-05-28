"""
Module: search_location_api
---------------------------

This module defines the FastAPI router and helper functions for performing
location-based searches and weather lookups using the OpenWeather API.

Endpoints:
- GET /weather
    Retrieves current weather information for a given input. Accepts city name,
    zip code, or GPS coordinates.

- POST /api/location/search
    Accepts partial or full location strings and returns a list of matching
    geographic locations.

Key Responsibilities:
- Normalize and detect user input types (lat/lon, zip, city name).
- Convert location strings to coordinates using the OpenWeather Geocoding API.
- Fetch current weather data using OpenWeather Weather API.
- Handle errors from third-party services gracefully and return meaningful
  error messages.

Integration Points:
- OpenWeather Geocoding and Weather APIs
- Environment variable handling via `dotenv`

This module enables fast, flexible search-based location lookups and real-time
weather data integration within the Weather App backend.
"""

import os
import re

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from requests.exceptions import RequestException

router = APIRouter()
load_dotenv()


def load_openweather_api_key() -> str:
    """
    Loads the OpenWeather API key from environment variables.

    Returns:
        str: The API key.

    Raises:
        RuntimeError: If the API key is not found in the environment.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY not set in environment variables.")
    return api_key


def geocode_location(location: str, api_key: str) -> tuple:
    """
    Converts a city name, address, or zip code to latitude and longitude using
    the OpenWeather Geocoding API.

    Args:
        location (str): City name, address, or zip code.
        api_key (str): OpenWeather API key.

    Returns:
        tuple: (latitude, longitude)

    Raises:
        ValueError: If the location is not found by the API.
        RequestException: If the API request fails.
    """
    try:
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={location}&limit=1&appid={api_key}"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"Location not found: {location}")
        return data[0]["lat"], data[0]["lon"]
    except RequestException as e:
        raise RuntimeError(f"Geocoding API request failed: {str(e)}") from e


def detect_input_type(user_input: str) -> str:
    """
    Detect the type of the input: 'latlon', 'zip', or 'city'.
    """
    if re.match(r"^-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?$", user_input.strip()):
        return "latlon"
    elif re.match(r"^\d{5}(-\d{4})?$", user_input.strip()):
        return "zip"
    return "city"


def parse_coordinates(input: str) -> tuple:
    """
    Parse latitude and longitude from a string input.
    """
    lat, lon = map(float, input.split(","))
    return lat, lon


def get_weather_by_coordinates(lat: float, lon: float, api_key: str) -> dict:
    """
    Get weather data from OpenWeather using latitude and longitude.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        api_key (str): OpenWeather API key.

    Returns:
        dict: Weather data from the API.

    Raises:
        RuntimeError: If the API request fails.
    """
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={api_key}"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        raise RuntimeError(f"Weather API request failed (latlon): {str(e)}") from e


def get_weather_by_zip(zip_code: str, api_key: str) -> dict:
    """
    Get weather data from OpenWeather using a zip code.

    Args:
        zip_code (str): Zip code, optionally with country code.
        api_key (str): OpenWeather API key.

    Returns:
        dict: Weather data from the API.

    Raises:
        RuntimeError: If the API request fails.
    """
    try:
        if "," not in zip_code:
            zip_code += ",KR"
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?zip={zip_code}&appid={api_key}"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        raise RuntimeError(f"Weather API request failed (zip): {str(e)}") from e


def resolve_input_and_fetch_weather(user_input: str, api_key: str) -> dict:
    """
    Resolve user input to a standard form and fetch weather data.
    """
    input_type = detect_input_type(user_input)
    if input_type == "latlon":
        lat, lon = parse_coordinates(user_input)
        return get_weather_by_coordinates(lat, lon, api_key)
    elif input_type == "zip":
        return get_weather_by_zip(user_input, api_key)
    else:
        lat, lon = geocode_location(user_input, api_key)
        return get_weather_by_coordinates(lat, lon, api_key)


@router.get("/weather")
def weather(user_input: str):
    """
    Retrieves current weather data based on user input.

    This endpoint supports input in the following formats:
    - City name (e.g., "Seoul")
    - ZIP code (e.g., "12345")
    - Latitude and longitude coordinates (e.g., "37.5665,126.978")

    Returns weather information in JSON format from OpenWeather API.
    """
    api_key = load_openweather_api_key()
    return resolve_input_and_fetch_weather(user_input, api_key)


@router.post("/api/location/search")
def search_location(
    query: str = Query(..., description="Partial or full location string to search."),
    limit: int = Query(5, ge=1, le=10, description="Max number of results to return."),
):
    """
    Searches for matching locations using a partial or full location string.

    This endpoint queries the OpenWeather geocoding API and returns a list of
    candidate locations based on the input query. The number of results can be
    limited using the `limit` parameter.

    Example usage:
    - query="Seoul" (returns geocoded information about Seoul)
    - query="Paris", limit=3 (returns top 3 matching locations for Paris)

    Returns:
        A dictionary containing a list of geocoded location results.
    """
    api_key = load_openweather_api_key()
    try:
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={query}&limit={limit}&appid={api_key}"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise HTTPException(status_code=404, detail="No matching locations found.")
        return {"results": data}
    except RequestException as e:
        raise HTTPException(status_code=502, detail=f"Geocoding API error: {str(e)}")
