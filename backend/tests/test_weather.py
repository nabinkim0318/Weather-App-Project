from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.main import app
from app.schemas.weather import (
    ForecastItem,
    ForecastResponse,
    WeatherBase,
    WeatherCurrent,
)

# Mocked Weather Data
mock_weather = WeatherCurrent(
    temp_c=22.5,
    temp_f=72.5,
    humidity=50.0,
    wind_speed=3.0,
    wind_deg=180,
    wind_gust=5.0,
    condition="Clear",
    condition_desc="clear sky",
    icon="01d",
    icon_url="/static/icons/01d.svg",
    sunrise=datetime.utcnow(),
    sunset=datetime.utcnow(),
    pressure=1012,
    visibility=10000,
    precipitation=None,
    precipitation_type=None,
    uvi=None,
    weather_code=800,
    updated_at=datetime.utcnow(),
)

mock_forecast = ForecastResponse(
    location=WeatherBase(
        city="Seoul", country="KR", latitude=37.5665, longitude=126.9780
    ),
    forecast=[
        ForecastItem(
            forecast_date=datetime.utcnow().date(),
            forecast_hour=datetime.utcnow().hour,
            temp_c=22.5,
            temp_f=72.5,
            condition="Clouds",
            condition_desc="few clouds",
            icon="02d",
            icon_url="/static/icons/02d.svg",
            precipitation=0.0,
            precipitation_type=None,
            updated_at=datetime.utcnow(),
            uvi=None,
            pressure=1010,
            wind_speed=3.0,
            wind_deg=180,
            wind_gust=4.0,
            humidity=40,
            visibility=10000,
            weather_code=801,
        )
    ],
)


@pytest.mark.asyncio
@patch("app.services.weather_service.fetch_current_weather", return_value=mock_weather)
async def test_get_current_weather(mock_fetch):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/weather/current?city=Seoul")
        assert response.status_code == 200
        assert "temp_c" in response.json()


@pytest.mark.asyncio
@patch("app.services.weather_service.fetch_forecast", return_value=mock_forecast)
async def test_get_forecast(mock_fetch):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/weather/forecast?city=Seoul")
        assert response.status_code == 200
        assert "forecast" in response.json()


@pytest.mark.asyncio
@patch("app.services.weather_service.fetch_current_weather", return_value=mock_weather)
async def test_get_weather_tip(mock_fetch):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/weather/summary?city=Seoul")
        assert response.status_code == 200
        assert "tip" in response.json()
