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


class WeatherHistoryBase(BaseModel):
    """
    This is the base model for weather records.

    Required fields:
    - location_id: Location ID (integer)
    - weather_date: Weather date (datetime)
    - temp_c: Temperature in Celsius (float)
    - temp_f: Temperature in Fahrenheit (float)
    - condition: Weather condition (string)

    Optional fields:
    - humidity: Humidity (float, 0-100)
    - wind_speed: Wind speed (float, m/s)
    - wind_deg: Wind direction (float, 0-360)
    - wind_gust: Wind gust speed (float, m/s)
    - condition_desc: Weather condition description
    - icon: Weather icon code
    - sunrise: Sunrise time
    - sunset: Sunset time
    - pressure: Pressure (hPa)
    - visibility: Visibility (km)
    - weather_code: Weather code
    - api_source: Data source
    - tip: Weather tip
    """

    location_id: int
    weather_date: datetime
    temp_c: float
    temp_f: float
    condition: str
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    condition_desc: Optional[str] = None
    icon: Optional[str] = None
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[float] = None
    precipitation_type: Optional[str] = None
    uvi: Optional[float] = None
    weather_code: Optional[int] = None
    api_source: Optional[str] = None
    tip: Optional[str] = None


class WeatherHistoryCreate(WeatherHistoryBase):
    """
    This is the schema for creating a new weather record.
    Inherits all fields from WeatherHistoryBase,
    location_id, weather_date, temp_c, temp_f, and condition are required fields.

    Example:
    {
        "location_id": 1,
        "weather_date": "2024-03-21T12:00:00",
        "temp_c": 20.5,
        "temp_f": 68.9,
        "condition": "Clear",
        "humidity": 65,
        "wind_speed": 3.5
    }
    """

    pass


class WeatherHistoryUpdate(WeatherHistoryBase):
    pass


class WeatherHistoryResponse(BaseModel):
    """
    Weather record retrieval response schema
    """

    id: int
    location_id: int
    weather_date: datetime
    temp_c: float
    temp_f: float
    condition: str
    humidity: float
    wind_speed: float
    created_at: datetime
    updated_at: Optional[datetime] = None

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


class HourlyWeather(BaseModel):
    hour: str
    timestamp: int
    temperature: float
    condition: str
    description: str
    icon: str


class HourlyWeatherResponse(BaseModel):
    location: str
    hourly_forecast: List[HourlyWeather]


# --------------------------
# Search Response
# --------------------------


class WeatherSearchResult(BaseModel):
    """
    Response schema for weather search results
    """

    location: WeatherBase
    current_weather: WeatherCurrent
    daily_forecast: Optional[List[ForecastItem]] = None
    hourly_forecast: Optional[List[HourlyWeather]] = None
    weather_tip: Optional[str] = None
    last_updated: datetime


class WeatherSearchResponse(BaseModel):
    """
    Response schema for search results
    """

    success: bool
    message: Optional[str] = None
    result: Optional[WeatherSearchResult] = None
    error: Optional[str] = None
