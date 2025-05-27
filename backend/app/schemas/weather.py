from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

# --------------------------
# Weather "Current" Response
# --------------------------


class WeatherBase(BaseModel):
    city: Optional[str]  # Geocoding API로 보완
    country: Optional[str]  # Geocoding API로 보완
    latitude: float
    longitude: float


class WeatherCondition(BaseModel):
    id: int  # weather code
    main: str  # e.g., "Clouds"
    description: str  # e.g., "broken clouds"
    icon: str  # e.g., "04d"


class WeatherCurrent(BaseModel):
    temp_c: float
    temp_f: float
    humidity: float
    wind_speed: float
    wind_deg: Optional[float]
    wind_gust: Optional[float]
    condition: str  # e.g., "Clouds"
    condition_desc: str  # e.g., "broken clouds"
    icon: str  # e.g., "04d"
    icon_url: Optional[str]  # 완성형 아이콘 URL (optional)
    sunrise: Optional[datetime]
    sunset: Optional[datetime]
    pressure: Optional[float]
    visibility: Optional[float]
    precipitation: Optional[float]  # rain.1h or snow.1h 등
    precipitation_type: Optional[Literal["rain", "snow"]]  # 강수 종류
    uvi: Optional[float]
    updated_at: datetime  # current.dt 기준
    weather_code: Optional[int]  # weather.id


class WeatherResponse(BaseModel):
    location: WeatherBase
    weather: WeatherCurrent


# --------------------------
# Forecast Response
# --------------------------


class ForecastItem(BaseModel):
    forecast_date: date
    forecast_hour: Optional[int] = None
    temp_c: float
    temp_f: float
    condition: str
    condition_desc: str
    icon: str
    icon_url: Optional[str]
    precipitation: Optional[float]
    precipitation_type: Optional[Literal["rain", "snow"]]
    uvi: Optional[float]
    pressure: Optional[float]
    wind_speed: Optional[float]
    wind_deg: Optional[float]
    wind_gust: Optional[float]
    humidity: Optional[float]
    visibility: Optional[float]
    weather_code: Optional[int]
    updated_at: datetime


class ForecastResponse(BaseModel):
    location: WeatherBase
    forecast: List[ForecastItem]


# --------------------------
# WeatherHistory (for DB fetch)
# --------------------------


class WeatherHistoryOut(BaseModel):
    id: int
    location_id: int
    weather_date: date
    temp_c: float
    temp_f: float
    humidity: float
    wind_speed: float
    wind_deg: Optional[float]
    wind_gust: Optional[float]
    condition: str
    condition_desc: str
    icon: str
    icon_url: Optional[str]
    sunrise: Optional[datetime]
    sunset: Optional[datetime]
    pressure: Optional[float]
    visibility: Optional[float]
    precipitation: Optional[float]
    precipitation_type: Optional[Literal["rain", "snow"]]
    uvi: Optional[float]
    weather_code: Optional[int]
    updated_at: datetime

    class Config:
        orm_mode = True


# --------------------------
# Create/Update Schemas (if needed)
# --------------------------


class WeatherCreate(BaseModel):
    location_id: int
    weather_date: date
    temp_c: float
    temp_f: float
    humidity: float
    wind_speed: float
    wind_deg: Optional[float]
    wind_gust: Optional[float]
    condition: str
    condition_desc: str
    icon: str
    icon_url: Optional[str]
    sunrise: Optional[datetime]
    sunset: Optional[datetime]
    pressure: Optional[float]
    visibility: Optional[float]
    precipitation: Optional[float]
    precipitation_type: Optional[Literal["rain", "snow"]]
    uvi: Optional[float]
    weather_code: Optional[int]
    updated_at: datetime
