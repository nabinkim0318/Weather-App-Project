from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseLocation(BaseModel):
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


# class CreateLocationRequest(BaseLocation):
#     is_favorite: bool = Field(False, description="Mark location as favorite")


class UpdateLocationRequest(BaseModel):
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
    id: int
    user_id: Optional[int]
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteToggleRequest(BaseModel):
    is_favorite: bool = Field(..., description="Set to true to mark as favorite")
