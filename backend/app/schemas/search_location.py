"""
schemas/search_location.py
---------------------------

Pydantic schemas for Location API endpoints.

This module defines request and response models for creating, updating,
retrieving, and toggling favorite user-defined locations. These schemas are
used in the Weather App backend to validate and document data exchanged
via FastAPI endpoints.

Includes:
- BaseLocation: Shared fields for location data.
- CreateLocationRequest: Schema for creating a new location.
- UpdateLocationRequest: Schema for partial updates.
- LocationResponse: Schema for returning saved locations.
- FavoriteToggleRequest: Schema for toggling favorite flag.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseLocation(BaseModel):
    """
    Base schema containing shared location fields.

    Used by CreateLocationRequest and LocationResponse for reusability and consistency.
    """

    label: str = Field(
        ..., max_length=100, description="User-given name for location (e.g., 'Home')"
    )
    city: str = Field(..., max_length=100, description="City name")
    state: Optional[str] = Field(
        None, max_length=100, description="State or province (optional)"
    )
    country: str = Field(..., max_length=100, description="Country name")
    postal_code: Optional[str] = Field(
        None, max_length=20, description="Zip or postal code (optional)"
    )
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(
        ..., ge=-180, le=180, description="Longitude (-180 to 180)"
    )


class CreateLocationRequest(BaseLocation):
    """
    Schema for creating a new location entry.

    Extends BaseLocation and adds the `is_favorite` flag.
    """

    is_favorite: bool = Field(False, description="Mark location as favorite")


class UpdateLocationRequest(BaseModel):
    """
    Schema for partially updating an existing location.

    All fields are optional to allow selective updates.
    """

    label: Optional[str] = Field(
        None, max_length=100, description="Updated location label"
    )
    is_favorite: Optional[bool] = Field(
        None, description="Set to true to mark as favorite"
    )
    city: Optional[str] = Field(None, max_length=100, description="Updated city name")
    state: Optional[str] = Field(
        None, max_length=100, description="Updated state or province"
    )
    country: Optional[str] = Field(
        None, max_length=100, description="Updated country name"
    )
    postal_code: Optional[str] = Field(
        None, max_length=20, description="Updated postal code"
    )
    latitude: Optional[float] = Field(
        None, ge=-90, le=90, description="Updated latitude"
    )
    longitude: Optional[float] = Field(
        None, ge=-180, le=180, description="Updated longitude"
    )


class LocationResponse(BaseLocation):
    """
    Schema for returning saved location data to the client.

    Includes metadata such as ID, user association, and creation timestamp.
    """

    id: int
    user_id: Optional[int]
    is_favorite: bool
    created_at: datetime

    class Config:
        orm_mode = True


class FavoriteToggleRequest(BaseModel):
    """
    Schema for toggling the favorite status of a saved location.
    """

    is_favorite: bool = Field(..., description="Set to true to mark as favorite")
