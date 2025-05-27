import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query

load_dotenv()

router = APIRouter()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


@router.get("/weather")
def get_weather(city: str = Query(...)):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code, detail=resp.json().get("message")
        )
    return resp.json()
