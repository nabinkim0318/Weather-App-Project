"""
Module: api.location
--------------------

This module defines the FastAPI router responsible for handling all location-related endpoints, including saving user locations,
searching for locations, managing favorite locations, and accessing search history. It provides CRUD functionality for user-associated
location data and interfaces with external geocoding services to validate and resolve locations.

Endpoints:
- POST /api/location/search
    Accepts partial or full location strings to perform fuzzy or exact location searches.
- POST /api/location/save
    Saves a new user location or updates an existing one in the database after validation.
- GET /api/location/favorites
    Retrieves a list of user's favorite locations.
- POST /api/location/favorites/add
    Adds a location to the user's favorites.
- POST /api/location/favorites/remove
    Removes a location from the user's favorites.
- GET /api/location/history
    Returns the user's recent location search history with timestamps.
- DELETE /api/location/history/{history_id}
    Deletes a specific search history record.

Key Responsibilities:
- Validate location input formats and ensure locations correspond to real-world places using external geocoding APIs.
- Manage user-specific location data persistence with appropriate database models.
- Support fuzzy search capabilities to handle partial or ambiguous location queries.
- Handle edge cases such as duplicate favorites, empty search results, and invalid location removals.
- Provide clear and descriptive error messages for validation, authorization, or not-found conditions.
- Ensure efficient and secure management of location data without requiring row-level user security.
- Support pagination or filtering of search history if the dataset grows large.

Integration Points:
- External geocoding services (e.g., Google Geocoding API, Mapbox, OpenStreetMap Nominatim)
- User authentication and authorization middleware (if applicable)
- Database CRUD operations for location, favorites, and history tables

This module facilitates robust user location management, enabling seamless integration of location-based services within the Weather App backend.
"""
from fastapi import APIRouter, Query

from app.services.weather_service import fetch_current_weather, fetch_forecast

router = APIRouter()