"""
Module: api.weather
-------------------

This module defines the FastAPI router responsible for handling all weather-
related endpoints, including current weather data retrieval, weather forecast
management, and integration with external weather APIs. It implements CRUD
operations to create, read, update, and delete weather data records in the
database, while also supporting fetching real-time weather information via
third-party APIs.

Endpoints:
- GET /api/weather/current
    Retrieves current weather information for a specified location.
- GET /api/weather/hourly
    Retrieves next 5 hours weather information for a specified location.
- POST /api/weather
    Creates new weather data entries based on a location and optional date
    range. Fetches data from external APIs and stores it persistently.
- GET /api/weather/{weather_id}
    Retrieves stored weather data by unique weather record identifier.
- PUT /api/weather/{weather_id}
    Updates specified fields of existing weather data entries with validation.
- DELETE /api/weather/{weather_id}
    Deletes weather data record identified by weather_id.
- GET /api/forecast
    Retrieves weather forecast data for a location and optionally a date range.
- Additional endpoints may support batch data retrieval, filtering, and aggregation.

Key Responsibilities:
- Validate user input for location formats, date ranges, and query parameters.
- Interact with external weather APIs to fetch real-time and forecast weather data.
- Persist weather data in a relational or NoSQL database with proper schema validation.
- Handle errors including validation failures, external API timeouts, data
  inconsistencies, and database transaction errors.
- Implement caching strategies for API responses to optimize performance.
- Return well-structured JSON responses conforming to Pydantic schemas.
- Support pagination and filtering for forecast data endpoints.

Integration Points:
- External Weather API providers (e.g., OpenWeatherMap, WeatherAPI, etc.)
- Database layer for CRUD operations on weather data.
- Authentication and authorization middleware (if applicable).

This module is a core part of the backend service enabling users and clients to
query, store, and manage weather-related information effectively.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import weather as crud
from app.schemas.weather import (
    ForecastResponse,
    HourlyWeatherResponse,
    WeatherCurrent,
    WeatherHistoryCreate,
    WeatherHistoryResponse,
    WeatherHistoryUpdate,
)
from app.services.weather_service import (
    fetch_current_weather,
    fetch_forecast,
    fetch_hourly_weather,
    get_weather_tip,
)

router = APIRouter(tags=["Weather"])


@router.get("/current", response_model=WeatherCurrent)
async def get_current_weather(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    zip_code: Optional[str] = Query(
        None, description="Zip code (postal code) of the location"
    ),
):
    try:
        # If zip code is provided, use it to get coordinates
        if zip_code:
            location = await get_location_by_zip(zip_code)
            if location:
                lat, lon = location["lat"], location["lon"]
            else:
                raise HTTPException(
                    status_code=404, detail="Location not found for the given zip code"
                )

        result = await fetch_current_weather(city=city, lat=lat, lon=lon)
        if not result:
            raise HTTPException(status_code=404, detail="Weather data not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    zip_code: Optional[str] = Query(
        None, description="Zip code (postal code) of the location"
    ),
    db: Session = Depends(get_db),
):
    try:
        # If zip code is provided, use it to get coordinates
        if zip_code:
            location = await get_location_by_zip(zip_code)
            if location:
                lat, lon = location["lat"], location["lon"]
            else:
                raise HTTPException(
                    status_code=404, detail="Location not found for the given zip code"
                )

        result = await fetch_forecast(city=city, lat=lat, lon=lon)
        if not result:
            raise HTTPException(status_code=404, detail="Forecast not available")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hourly", response_model=HourlyWeatherResponse)
async def get_hourly_weather(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    zip_code: Optional[str] = Query(
        None, description="Zip code (postal code) of the location"
    ),
):
    """
    Fetch hourly weather data for the next 5 hours for a specified location.
    Location can be specified by city name, coordinates (lat/lon), or zip code.
    """
    try:
        # If zip code is provided, use it to get coordinates
        if zip_code:
            location = await get_location_by_zip(zip_code)
            if location:
                lat, lon = location["lat"], location["lon"]
            else:
                raise HTTPException(
                    status_code=404, detail="Location not found for the given zip code"
                )

        result = await fetch_hourly_weather(city=city, lat=lat, lon=lon)
        if not result:
            raise HTTPException(status_code=404, detail="Hourly weather data not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_location_by_zip(zip_code: str) -> Optional[dict]:
    """
    Converts a zip code to coordinates using location search service.
    Returns a dictionary containing latitude and longitude if found.
    """
    try:
        # Use the existing location search service
        from app.services.location_service import search_location

        # Search for the location using zip code
        locations = await search_location(zip_code)
        if locations and len(locations) > 0:
            # Return the first matching location's coordinates
            return {"lat": locations[0]["lat"], "lon": locations[0]["lon"]}
        return None
    except Exception as e:
        print(f"Error searching location: {str(e)}")
        return None


@router.post("", response_model=dict)
def store_weather(data: WeatherHistoryCreate, db: Session = Depends(get_db)):
    try:
        record = crud.create_weather_record(db, data)
        return {"id": record.id, "message": "Weather data stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[WeatherHistoryResponse])
def get_weather_history(location_id: int, db: Session = Depends(get_db)):
    """
    Search for weather history for a specific location.
    """
    return crud.get_weather_by_location(db, location_id)


@router.get("/summary", response_model=dict)
async def weather_tip(city: Optional[str] = Query(None)):
    result = await fetch_current_weather(city=city)
    if result is None:
        raise HTTPException(status_code=404, detail="Weather data not found.")
    tip = get_weather_tip(result.condition)
    return {"tip": tip}


@router.get("/airquality", response_model=dict)
def dummy_air_quality():
    return {"message": "Air quality endpoint not implemented yet."}


@router.get("/{weather_id}", response_model=WeatherHistoryResponse)
def get_weather_by_id(weather_id: int, db: Session = Depends(get_db)):
    weather = crud.get_weather_by_id(db, weather_id)
    if not weather:
        raise HTTPException(status_code=404, detail="Weather record not found")
    return weather


@router.put("/{weather_id}", response_model=WeatherHistoryResponse)
def update_weather(
    weather_id: int, data: WeatherHistoryUpdate, db: Session = Depends(get_db)
):
    try:
        record = crud.update_weather_record(db, weather_id, data)
        if not record:
            raise HTTPException(status_code=404, detail="Weather record not found")
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{weather_id}", response_model=dict)
def delete_weather(weather_id: int, db: Session = Depends(get_db)):
    success = crud.delete_weather_record(db, weather_id)
    if not success:
        raise HTTPException(status_code=404, detail="Deletion failed; record not found")
    return {"message": "Record deleted successfully."}
