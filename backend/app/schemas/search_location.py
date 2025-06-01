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


class SearchLocationBase(BaseModel):
    label: Optional[str] = None
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    latitude: float
    longitude: float


class SearchLocationCreate(SearchLocationBase):
    pass


class SearchLocationUpdate(SearchLocationBase):
    pass


class SearchLocationResponse(SearchLocationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class FavoriteToggleRequest(BaseModel):
    """
    Schema for toggling the favorite status of a saved location.
    """

    is_favorite: bool = Field(..., description="Set to true to mark as favorite")


class LocationBase(BaseModel):
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    label: str
    user_id: Optional[int] = None


class SearchHistoryResponse(BaseModel):
    id: int
    query: str
    searched_at: datetime

    class Config:
        from_attributes = True
