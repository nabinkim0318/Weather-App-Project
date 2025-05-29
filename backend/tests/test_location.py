from typing import Tuple
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import RequestException

# Sample input-output for mocking
mock_geo_response = [{"name": "Seoul", "lat": 37.5665, "lon": 126.978, "country": "KR"}]

mock_weather_response = {
    "weather": [{"description": "clear sky"}],
    "main": {"temp": 289.92},
    "name": "Seoul",
}


def test_detect_input_type():
    from backend.app.api.search_location import detect_input_type

    assert detect_input_type("37.5665,126.978") == "latlon"
    assert detect_input_type("12345") == "zip"
    assert detect_input_type("Seoul") == "city"


def test_parse_coordinates():
    from backend.app.api.search_location import parse_coordinates

    assert parse_coordinates("37.5665,126.978") == (37.5665, 126.978)


@patch("requests.get")
def test_geocode_location_success(mock_get):
    from backend.app.api.search_location import geocode_location

    mock_response = Mock()
    mock_response.json.return_value = mock_geo_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    lat, lon = geocode_location("Seoul", "dummy_key")
    assert lat == 37.5665 and lon == 126.978


@patch("requests.get", side_effect=RequestException("API error"))
def test_geocode_location_failure(mock_get):
    from backend.app.api.search_location import geocode_location

    with pytest.raises(RuntimeError, match="Geocoding API request failed"):
        geocode_location("Nowhere", "dummy_key")


@patch("requests.get")
def test_get_weather_by_coordinates(mock_get):
    from backend.app.api.search_location import get_weather_by_coordinates

    mock_response = Mock()
    mock_response.json.return_value = mock_weather_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    data = get_weather_by_coordinates(37.5665, 126.978, "dummy_key")
    assert data["name"] == "Seoul"


@patch("requests.get", side_effect=RequestException("Network error"))
def test_get_weather_by_zip_failure(mock_get):
    from backend.app.api.search_location import get_weather_by_zip

    with pytest.raises(RuntimeError, match="Weather API request failed"):
        get_weather_by_zip("12345", "dummy_key")


# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.models.user_location import UserLocation
# from app.services import user_location as svc
# from app.db.database import Base

# # Set up in-memory test DB
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="module")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()

# def test_save_user_location(test_db):
#     user_id = 1
#     location = UserLocation(
#         label="Home",
#         city="Seoul",
#         state="Seoul",
#         country="KR",
#         postal_code="12345",
#         latitude=37.5665,
#         longitude=126.9780,
#         user_id=user_id
#     )
#     test_db.add(location)
#     test_db.commit()
#     test_db.refresh(location)

#     # Convert to dict for comparison
#     location_dict = {
#         'label': location.label,
#         'city': location.city,
#         'latitude': float(location.latitude),
#         'longitude': float(location.longitude),
#     }

#     expected = {
#         'label': 'Home',
#         'city': 'Seoul',
#         'latitude': 37.5665,
#         'longitude': 126.9780,
#     }

#     assert location_dict == expected

# def test_get_locations_by_user(test_db):
#     locations = svc.get_locations_by_user(test_db, user_id=1)
#     assert len(locations) == 1
#     assert locations[0].city == "Seoul"
