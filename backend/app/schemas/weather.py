from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

# --------------------------
# Location Metadata
# --------------------------


class WeatherBase(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# --------------------------
# Weather Condition Detail
# --------------------------
class WeatherCondition(BaseModel):
    id: int  # weather code
    main: str  # e.g., "Clouds"
    description: str  # e.g., "broken clouds"
    icon: str  # e.g., "04d"


# --------------------------
# Current Weather Request/Response
# --------------------------
class WeatherRequest(BaseModel):
    location: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class WeatherCurrent(BaseModel):
    temp_c: float
    temp_f: float
    humidity: float
    wind_speed: float
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    condition: str
    condition_desc: str
    icon: str
    icon_url: Optional[str] = None
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[float] = None
    precipitation_type: Optional[Literal["rain", "snow"]] = None
    uvi: Optional[float] = None
    weather_code: Optional[int] = None
    updated_at: datetime


class WeatherResponse(BaseModel):
    location: WeatherBase
    weather: WeatherCurrent


class WeatherDetailResponse(BaseModel):
    location: WeatherBase
    weather: WeatherCurrent
    tip: Optional[str] = None
    api_source: Optional[str] = None
    raw_response: Optional[dict] = None


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
    icon_url: Optional[str] = None
    precipitation: Optional[float] = None
    precipitation_type: Optional[Literal["rain", "snow"]] = None
    uvi: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    humidity: Optional[float] = None
    visibility: Optional[float] = None
    weather_code: Optional[int] = None
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
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    condition: str
    condition_desc: str
    icon: str
    icon_url: Optional[str] = None
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[float] = None
    precipitation_type: Optional[Literal["rain", "snow"]] = None
    uvi: Optional[float] = None
    weather_code: Optional[int] = None
    updated_at: datetime

    class Config:
        from_attributes = True


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
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    condition: str
    condition_desc: str
    icon: str
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[float] = None
    precipitation_type: Optional[Literal["rain", "snow"]] = None
    uvi: Optional[float] = None
    weather_code: Optional[int] = None
    updated_at: datetime


class WeatherUpdate(BaseModel):
    temp_c: Optional[float] = None
    temp_f: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    condition: Optional[str] = None
    condition_desc: Optional[str] = None
    icon: Optional[str] = None
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[float] = None
    precipitation_type: Optional[Literal["rain", "snow"]] = None
    uvi: Optional[float] = None
    weather_code: Optional[int] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --------------------------
# Summary / Tip of the Day
# --------------------------


class WeatherSummaryResponse(BaseModel):
    tip: str
    condition: str
    icon: Optional[str] = None
    location: WeatherBase
    date: date


class WeatherSearchHistoryItem(BaseModel):
    query: str
    searched_at: datetime


class SavedLocation(BaseModel):
    id: int
    label: str
    city: str
    country: str
    latitude: float
    longitude: float
    is_favorite: bool
    created_at: datetime
