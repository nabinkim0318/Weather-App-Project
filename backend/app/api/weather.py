"""
Module: api.weather
-------------------

This module defines the FastAPI router responsible for handling all weather-related endpoints, including current weather data retrieval,
weather forecast management, and integration with external weather APIs. It implements CRUD operations to create, read, update, and delete
weather data records in the database, while also supporting fetching real-time weather information via third-party APIs.

Endpoints:
- GET /api/weather/current
    Retrieves current weather information for a specified location.
- POST /api/weather
    Creates new weather data entries based on a location and optional date range. Fetches data from external APIs and stores it persistently.
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
- Handle errors including validation failures, external API timeouts, data inconsistencies, and database transaction errors.
- Implement caching strategies for API responses to optimize performance.
- Return well-structured JSON responses conforming to Pydantic schemas.
- Support pagination and filtering for forecast data endpoints.

Integration Points:
- External Weather API providers (e.g., OpenWeatherMap, WeatherAPI, etc.)
- Database layer for CRUD operations on weather data.
- Authentication and authorization middleware (if applicable).

This module is a core part of the backend service enabling users and clients to query, store, and manage weather-related information effectively.
"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from pydantic import BaseModel, Field, field_validator

from app.services.weather_service import (delete_weather_data,
                                          fetch_current_weather,
                                          fetch_forecast, get_forecast_data,
                                          get_weather_by_id, save_weather_data,
                                          update_weather_data)

router = APIRouter()


# --- Pydantic Schema Example -


class WeatherCreateRequest(BaseModel):
    city: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    start_date: Optional[date]
    end_date: Optional[date]

    @field_validator("start_date", "end_date")
    @classmethod
    def valid_dates(cls, v):
        if v and v > date.today():
            raise ValueError("Date cannot be in the future")
        return v

    @field_validator("end_date")
    @classmethod
    def check_date_range(cls, v, values):
        if "start_date" in values.data and values.data["start_date"] and v:
            if v < values.data["start_date"]:
                raise ValueError("end_date must be after start_date")
        return v


class WeatherResponse(BaseModel):
    id: int
    city: str
    lat: float
    lon: float
    date: date
    temperature: float
    condition: str


class ForecastResponse(BaseModel):
    city: str
    lat: float
    lon: float
    forecast: List[WeatherResponse]


# --- Endpoint Implementation ---


@router.get("/weather/current", response_model=WeatherResponse)
def get_current_weather(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    result = fetch_current_weather(city, lat, lon)
    if not result:
        raise HTTPException(status_code=404, detail="Weather not found.")
    return result


@router.post(
    "/weather", response_model=WeatherResponse, status_code=status.HTTP_201_CREATED
)
def create_weather(data: WeatherCreateRequest = Body(...)):
    # Fetch weather data from external API and save to DB
    saved = save_weather_data(data)
    if not saved:
        raise HTTPException(status_code=500, detail="Failed to save weather data.")
    return saved


@router.get("/weather/{weather_id}", response_model=WeatherResponse)
def read_weather(weather_id: int = Path(..., gt=0)):
    data = get_weather_by_id(weather_id)
    if not data:
        raise HTTPException(status_code=404, detail="Weather record not found.")
    return data


@router.put("/weather/{weather_id}", response_model=WeatherResponse)
def update_weather(weather_id: int, data: WeatherCreateRequest):
    updated = update_weather_data(weather_id, data)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Weather record not found or update failed."
        )
    return updated


@router.delete("/weather/{weather_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weather(weather_id: int):
    success = delete_weather_data(weather_id)
    if not success:
        raise HTTPException(status_code=404, detail="Weather record not found.")
    return None


@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    forecast = get_forecast_data(city, lat, lon, start_date, end_date, page, page_size)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found.")
    return forecast
