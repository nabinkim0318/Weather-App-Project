from fastapi import APIRouter, Query

from app.services.weather_service import fetch_current_weather, fetch_forecast

router = APIRouter()


@router.get("/weather")
def get_weather(
    city: str = Query(None), lat: float = Query(None), lon: float = Query(None)
):
    result = fetch_current_weather(city, lat, lon)
    if not result:
        return {"detail": "Weather not found."}
    return result


@router.get("/forecast")
def get_forecast(
    city: str = Query(None), lat: float = Query(None), lon: float = Query(None)
):
    result = fetch_forecast(city, lat, lon)
    if not result:
        return {"detail": "Forecast not found."}
    return result
