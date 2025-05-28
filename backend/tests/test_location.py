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
