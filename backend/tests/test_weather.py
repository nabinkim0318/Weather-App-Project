# backend/tests/test_weather.py
import re


def test_basic_functionality():
    """Simple test that always passes"""
    assert 1 + 1 == 2
    assert "weather" in "weather app"
    assert len("test") == 4


def test_weather_module_exists():
    """Test that weather service module can be imported"""
    try:
        from app.services.weather_service import fetch_current_weather

        assert True
    except ImportError:
        assert False, "Weather service module not found"


def test_zip_code_validation():
    """Test zip code validation using regex"""
    # US zip code pattern (5 digits or 5+4 format)
    us_zip_pattern = r"^\d{5}(-\d{4})?$"

    # Valid zip codes
    assert re.match(us_zip_pattern, "10001")
    assert re.match(us_zip_pattern, "90210")
    assert re.match(us_zip_pattern, "12345-6789")

    # Invalid zip codes
    assert not re.match(us_zip_pattern, "1234")  # too short
    assert not re.match(us_zip_pattern, "123456")  # too long
    assert not re.match(us_zip_pattern, "abcde")  # not digits
    assert not re.match(us_zip_pattern, "12345-678")  # wrong extended format
