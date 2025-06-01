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
from typing import List, Optional

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import SearchLocation, WeatherHistory
from app.models.search_history import SearchHistory
from app.schemas.search_location import (
    SearchHistoryResponse,
    SearchLocationCreate,
    SearchLocationResponse,
    SearchLocationUpdate,
)

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


def validate_zip_code(zip_code: str) -> bool:
    """
    Validate ZIP code format.

    Args:
        zip_code (str): ZIP code to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # US ZIP code: 5 digits or 5+4 format
    return bool(re.match(r"^\d{5}(-\d{4})?$", zip_code.strip()))


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


def get_weather_by_zip(zip_code: str, api_key: str) -> tuple:
    """
    Converts a zip code to latitude and longitude using OpenWeather APIs.

    Args:
        zip_code (str): ZIP code to convert
        api_key (str): OpenWeather API key

    Returns:
        tuple: (latitude, longitude)

    Raises:
        ValueError: If ZIP code format is invalid
        RuntimeError: If API request fails or ZIP code not found
    """
    # First validate ZIP code format
    if not validate_zip_code(zip_code):
        raise ValueError(f"{zip_code} is not valid")

    try:
        # Use the dedicated ZIP endpoint
        if "," not in zip_code:
            zip_code += ",US"  # default country code
        zip_url = (
            f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
        )
        response = requests.get(zip_url, timeout=5)

        if response.status_code == 404:
            # Extract the original zip code without country code for error message
            original_zip = zip_code.split(",")[0]
            raise ValueError(f"{original_zip} is not valid")

        response.raise_for_status()
        data = response.json()
        return data["lat"], data["lon"]

    except ValueError:
        # Re-raise ValueError as is
        raise
    except RequestException as e:
        if "404" in str(e):
            original_zip = zip_code.split(",")[0]
            raise ValueError(f"{original_zip} is not valid")
        raise RuntimeError(f"Geocoding API request failed: {str(e)}") from e


def resolve_input_and_fetch_weather(user_input: str, api_key: str) -> dict:
    """
    Resolve user input to a standard form and fetch weather data.

    Args:
        user_input (str): User input (city, zip code, or coordinates)
        api_key (str): OpenWeather API key

    Returns:
        dict: Weather data from the API

    Raises:
        ValueError: If input format is invalid (e.g., invalid zip code)
        RuntimeError: If API request fails
    """
    input_type = detect_input_type(user_input)
    if input_type == "latlon":
        lat, lon = parse_coordinates(user_input)
        return get_weather_by_coordinates(lat, lon, api_key)
    elif input_type == "zip":
        lat, lon = get_weather_by_zip(user_input, api_key)
        return get_weather_by_coordinates(lat, lon, api_key)
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
    try:
        api_key = load_openweather_api_key()
        return resolve_input_and_fetch_weather(user_input, api_key)
    except ValueError as e:
        # Handle invalid input format (e.g., invalid zip code)
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        # Handle API request failures
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/search")
async def search_location(
    query: str = Query(..., description="Partial or full location string to search."),
    limit: int = Query(5, ge=1, le=10, description="Max number of results to return."),
    db: Session = Depends(get_db),
):
    """
    Search locations and save search history.
    If already saved location, return the information,
    if not, call OpenWeather API to save the new location.
    """
    api_key = load_openweather_api_key()
    try:
        # 1. Search Location First, Search Local DB
        local_results = (
            db.query(SearchLocation)
            .filter(
                SearchLocation.city.ilike(f"%{query}%")
                | SearchLocation.state.ilike(f"%{query}%")
                | SearchLocation.postal_code.ilike(f"%{query}%")
            )
            .limit(limit)
            .all()
        )

        # If found in Local DB, return the result
        if local_results:
            return {
                "results": [
                    {
                        "id": loc.id,
                        "name": loc.city,
                        "state": loc.state,
                        "country": loc.country,
                        "lat": loc.latitude,
                        "lon": loc.longitude,
                        "postal_code": loc.postal_code,
                    }
                    for loc in local_results
                ]
            }

        # 2. If not found in Local DB, call OpenWeather API
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={query}&limit={limit}&appid={api_key}"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise HTTPException(status_code=404, detail="No matching locations found.")

        # 3. Save the search result to DB
        saved_locations = []
        for location in data:
            # Check for duplicates by latitude/longitude
            existing_location = (
                db.query(SearchLocation)
                .filter(
                    SearchLocation.latitude == location.get("lat"),
                    SearchLocation.longitude == location.get("lon"),
                )
                .first()
            )

            if not existing_location:
                new_location = SearchLocation(
                    city=location.get("name", ""),
                    state=location.get("state"),
                    country=location.get("country", ""),
                    latitude=location.get("lat"),
                    longitude=location.get("lon"),
                    external_id=str(location.get("id")) if "id" in location else None,
                )
                db.add(new_location)
                db.commit()
                db.refresh(new_location)
                saved_locations.append(new_location)
            else:
                saved_locations.append(existing_location)

        # 4. Save the search history
        search_record = SearchHistory(user_id=1, query=query)  # Temporary user ID
        db.add(search_record)
        db.commit()

        return {
            "results": [
                {
                    "id": loc.id,
                    "name": loc.city,
                    "state": loc.state,
                    "country": loc.country,
                    "lat": loc.latitude,
                    "lon": loc.longitude,
                    "postal_code": loc.postal_code,
                }
                for loc in saved_locations
            ]
        }
    except RequestException as e:
        db.rollback()
        raise HTTPException(status_code=502, detail=f"Geocoding API error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error occurred while searching: {str(e)}"
        )


@router.get("/history", response_model=List[SearchHistoryResponse])
async def get_search_history(db: Session = Depends(get_db)):
    """
    Retrieve the latest search history.
    """
    try:
        # Get the latest 10 search history
        history = (
            db.query(SearchHistory)
            .order_by(SearchHistory.searched_at.desc())
            .limit(10)
            .all()
        )

        return history
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while retrieving search history: {str(e)}",
        )


@router.post("/locations", response_model=SearchLocationResponse)
async def create_location(
    location_data: SearchLocationCreate, db: Session = Depends(get_db)
):
    """
    Create a new location record.
    """
    try:
        # Check for duplicates
        existing = (
            db.query(SearchLocation)
            .filter(
                SearchLocation.city == location_data.city,
                SearchLocation.country == location_data.country,
                SearchLocation.state == location_data.state,
            )
            .first()
        )

        if existing:
            raise HTTPException(status_code=409, detail="Location already exists")

        # Create new location
        new_location = SearchLocation(**location_data.dict())
        db.add(new_location)
        db.commit()
        db.refresh(new_location)

        return new_location
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/locations", response_model=List[SearchLocationResponse])
async def get_all_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    city: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get all location records with optional filtering.
    """
    query = db.query(SearchLocation)

    if city:
        query = query.filter(SearchLocation.city.ilike(f"%{city}%"))
    if country:
        query = query.filter(SearchLocation.country.ilike(f"%{country}%"))

    locations = query.offset(skip).limit(limit).all()
    return locations


@router.get("/locations/{location_id}", response_model=SearchLocationResponse)
async def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    """
    Get a specific location by ID.
    """
    location = db.query(SearchLocation).filter(SearchLocation.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=404, detail=f"Location with ID {location_id} not found"
        )
    return location


@router.put("/locations/{location_id}", response_model=SearchLocationResponse)
async def update_location(
    location_id: int, location_data: SearchLocationUpdate, db: Session = Depends(get_db)
):
    """
    Update a specific location.
    """
    try:
        location = (
            db.query(SearchLocation).filter(SearchLocation.id == location_id).first()
        )
        if not location:
            raise HTTPException(
                status_code=404, detail=f"Location with ID {location_id} not found"
            )

        # 업데이트 데이터 적용
        for field, value in location_data.dict(exclude_unset=True).items():
            setattr(location, field, value)

        db.commit()
        db.refresh(location)
        return location
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/locations/{location_id}")
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific location.
    """
    try:
        location = (
            db.query(SearchLocation).filter(SearchLocation.id == location_id).first()
        )
        if not location:
            raise HTTPException(
                status_code=404, detail=f"Location with ID {location_id} not found"
            )

        # Check if there are any weather records associated with this location
        weather_count = (
            db.query(WeatherHistory)
            .filter(WeatherHistory.location_id == location_id)
            .count()
        )

        if weather_count > 0:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Cannot delete location. {weather_count} weather records"
                    "are associated with this location."
                ),
            )

        db.delete(location)
        db.commit()
        return {"message": f"Location with ID {location_id} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
