import os
from unittest.mock import patch

import pytest

from app.api.location import geocode_location


def test_geocode_location_success():
    # Mocked API response data for "Seoul"
    mock_response = [
        {"name": "Seoul", "lat": 37.5665, "lon": 126.9780, "country": "KR"}
    ]
    with patch("app.api.location.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        os.environ["OPENWEATHER_API_KEY"] = "dummy_key"
        lat, lon = geocode_location("Seoul")
        assert lat == 37.5665
        assert lon == 126.9780


def test_geocode_location_not_found():
    with patch("app.api.location.requests.get") as mock_get:
        mock_get.return_value.json.return_value = []
        os.environ["OPENWEATHER_API_KEY"] = "dummy_key"
        with pytest.raises(ValueError) as excinfo:
            geocode_location("InvalidCityName")
        assert "Location not found" in str(excinfo.value)


def test_geocode_location_missing_api_key():
    with patch("app.api.location.requests.get"):
        if "OPENWEATHER_API_KEY" in os.environ:
            del os.environ["OPENWEATHER_API_KEY"]
        with pytest.raises(RuntimeError) as excinfo:
            geocode_location("Seoul")
        assert "OPENWEATHER_API_KEY not set" in str(excinfo.value)
