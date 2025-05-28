"""
Module: user_location_api
--------------------------

This module defines the FastAPI router and database interaction logic for managing
user-specific location data within the Weather App backend.

Endpoints:
- POST /api/location/save
    Save a new user location or update an existing one.

- GET /api/location/favorites
    Retrieve the list of a user's favorite locations.

- POST /api/location/favorites/add
    Add a location to the user's favorites.

- POST /api/location/favorites/remove
    Remove a location from the user's favorites.

- GET /api/location/history
    Fetch the user's recent location search history.

- DELETE /api/location/history/{history_id}
    Delete a specific record from the user's search history.

Key Responsibilities:
- Persist and query user-associated location data using the database.
- Ensure idempotent creation and updating of user locations.
- Prevent duplicate entries in favorites and history.
- Handle invalid location removals gracefully.
- Support pagination and filtering of large search history datasets.
- Integrate with authentication/authorization middleware if needed.

Integration Points:
- Database models for `UserLocation`, `FavoriteLocation`, `SearchHistory`
- Optional user authentication for associating data per account
- Error handling for edge cases like duplicate inserts or not-found deletions

This module provides persistent, user-centered location services essential
for personalization and usability of the Weather App.
"""
