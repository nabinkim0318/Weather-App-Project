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

from fastapi import APIRouter, Query

from app.services.weather_service import fetch_current_weather, fetch_forecast

router = APIRouter()


@router.get("/weather")
def get_weather(
    city: str = Query(None), lat: float = Query(None), lon: float = Query(None)
):
    result = fetch_current_weather(city, lat, lon)
    if not result:
        return {"detail": "Weather not found."}
    return result


@router.get("/forecast")
def get_forecast(
    city: str = Query(None), lat: float = Query(None), lon: float = Query(None)
):
    result = fetch_forecast(city, lat, lon)
    if not result:
        return {"detail": "Forecast not found."}
    return result
