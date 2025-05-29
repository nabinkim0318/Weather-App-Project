# from typing import List

# from fastapi import APIRouter, Depends, HTTPException, Path
# from sqlalchemy.orm import Session

# from app.db.database import get_db  # your database session dependency
# from app.models.user_location import UserLocation
# from app.schemas.user_location import (
#     #CreateLocationRequest,
#     FavoriteToggleRequest,
#     LocationResponse,
#     UpdateLocationRequest,
# )
# from app.services import user_location as svc
# from crud import user_location as crud


# import os

# from dotenv import load_dotenv

# # Load .env from the project root
# load_dotenv(
#     dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# )

# """
# Module: user_location_api
# --------------------------

# This module defines the FastAPI router and database interaction logic for managing
# user-specific location data within the Weather App backend.

# Endpoints:
# - POST /api/location
#     Save a new user location.

# - GET /api/location/user/{user_id}
#     Retrieve the list of a user's saved locations.

# - PATCH /api/location/{location_id}
#     Update a saved location.

# - PATCH /api/location/{location_id}/favorite
#     Toggle a location's favorite status.

# - DELETE /api/location/{location_id}
#     Delete a user-saved location.

# Key Responsibilities:
# - Persist and query user-associated location data using the database.
# - Ensure idempotent creation and updating of user locations.
# - Prevent duplicate entries in favorites.
# - Handle invalid location updates or removals gracefully.

# Integration Points:
# - Database models for `UserLocation` and related entities
# - Error handling for edge cases like duplicate inserts or not-found deletions

# This module provides persistent, user-centered location services essential
# for personalization and usability of the Weather App.
# """

# router = APIRouter()


# @router.post("/api/location", response_model=LocationResponse)
# def create_location(
#     user_id: int, location: CreateLocationRequest, db: Session = Depends(get_db)
# ):
#     """
#     Create a new location entry in the database.

#     Args:
#         location (CreateLocationRequest): The location data to save.
#         db (Session): Database session.

#     Returns:
#         LocationResponse: The created location with metadata.
#     """
#     return svc.save_user_location(db, user_id, location)


# @router.get("/api/location/user/{user_id}", response_model=List[LocationResponse])
# def get_user_locations(
#     user_id: int = Path(..., description="ID of the user whose locations to
#          retrieve"),
#     db: Session = Depends(get_db),
# ):
#     """
#     Retrieve all saved locations for a specific user.

#     Args:
#         user_id (int): The ID of the user.
#         db (Session): Database session.

#     Returns:
#         List[LocationResponse]: A list of the user's saved locations.
#     """
#     return svc.get_locations_by_user(db, user_id)


# @router.patch("/api/location/{location_id}", response_model=LocationResponse)
# def update_location(
#     location_id: int,
#     location_update: UpdateLocationRequest,
#     db: Session = Depends(get_db),
# ):
#     """
#     Update an existing location with new data.

#     Args:
#         location_id (int): The ID of the location to update.
#         location_update (UpdateLocationRequest): The fields to update.
#         db (Session): Database session.

#     Returns:
#         LocationResponse: The updated location.

#     Raises:
#         HTTPException: If the location is not found.
#     """
#     updated = crud.update_location(db, location_id, location_update)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Location not found")
#     return updated


# @router.patch("/api/location/{location_id}/favorite", response_model=LocationResponse)
# def toggle_favorite(
#     location_id: int, toggle: FavoriteToggleRequest, db: Session = Depends(get_db)
# ):
#     """
#     Toggle the favorite status of a location.

#     Args:
#         location_id (int): The ID of the location.
#         toggle (FavoriteToggleRequest): Whether to mark as favorite.
#         db (Session): Database session.

#     Returns:
#         LocationResponse: The updated location with favorite status.

#     Raises:
#         HTTPException: If the location is not found.
#     """
#     updated = crud.toggle_favorite(db, location_id, toggle.is_favorite)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Location not found")
#     return updated


# @router.delete("/api/location/{location_id}")
# def delete_location(location_id: int, db: Session = Depends(get_db)):
#     """
#     Delete a location by its ID.

#     Args:
#         location_id (int): The ID of the location to delete.
#         db (Session): Database session.

#     Returns:
#         dict: A message confirming deletion.

#     Raises:
#         HTTPException: If the location is not found.
#     """
#     deleted = crud.delete_location(db, location_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Location not found")
#     return {"message": "Location deleted successfully"}
