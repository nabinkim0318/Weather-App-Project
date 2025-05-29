"""
Module: models.weather
----------------------

This module defines ORM models related to weather data within the application's
database schema. It provides structured mapping for weather-related entities such as
current weather records, historical weather data, and weather forecasts, enabling
persistent storage, querying, and management of weather information.

Key Responsibilities:
- Define tables/models for storing weather observations and forecasts with relevant
  meteorological fields:
  - Temperature (Celsius and Fahrenheit)
  - Humidity, wind speed, wind direction, wind gusts
  - Atmospheric pressure, visibility, precipitation amount and type
  - UV index, sunrise and sunset times
  - Weather condition descriptions and icons
  - Timestamp fields for when data was observed or updated
- Establish foreign key relationships linking weather records to specific locations
  (referencing the Location model) for spatial association.
- Enforce indexing on commonly queried fields such as location ID and timestamp for
  performance optimization.
- Provide support for storing multiple types of weather data:
  - Current weather snapshots
  - Historical weather records (time series)
  - Forecasted weather data (daily, hourly)
- Facilitate CRUD operations on weather data with consistency & integrity guarantees.
- Enable integration with weather APIs by storing raw or processed response data.
- Support data versioning or update tracking through timestamp fields.

Usage:
- Use the WeatherHistory model for storing & retrieving historical weather observations.
- Use the Forecast model (if defined) to save forecast data for locations and dates.
- Access weather data linked to locations for API response construction or UI rendering.
- Enable weather data updates with validation and error handling in services.

Benefits:
- Centralized and normalized storage of weather data to avoid redundancy.
- Improved query performance via indexing and relational design.
- Supports complex queries across time and location dimensions.
- Scalable design to handle high-volume weather data ingestion.

Example:
```python
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"),
       nullable=False, index=True)
    weather_date = Column(DateTime, nullable=False, index=True)
    temp_c = Column(Float, nullable=False)
    temp_f = Column(Float, nullable=False)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Float, nullable=True)
    wind_gust = Column(Float, nullable=True)
    condition = Column(String, nullable=False)
    condition_desc = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    sunrise = Column(DateTime, nullable=True)
    sunset = Column(DateTime, nullable=True)
    pressure = Column(Float, nullable=True)
    visibility = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    precipitation_type = Column(String, nullable=True)
    uvi = Column(Float, nullable=True)
    weather_code = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=False)

    location = relationship("Location", back_populates="weather_records")
"""

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base  # Usually declared in database.py


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(
        Integer, ForeignKey("locations.id"), nullable=False, index=True
    )
    weather_date = Column(DateTime, nullable=False, index=True)

    temp_c = Column(Float, nullable=False)
    temp_f = Column(Float, nullable=False)
    humidity = Column(Float, nullable=True)

    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Float, nullable=True)
    wind_gust = Column(Float, nullable=True)

    condition = Column(String, nullable=False)
    condition_desc = Column(String, nullable=True)
    icon = Column(String, nullable=True)

    sunrise = Column(DateTime, nullable=True)
    sunset = Column(DateTime, nullable=True)

    pressure = Column(Float, nullable=True)
    visibility = Column(Float, nullable=True)

    precipitation = Column(Float, nullable=True)
    precipitation_type = Column(String, nullable=True)

    uvi = Column(Float, nullable=True)
    weather_code = Column(Integer, nullable=True)

    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    location = relationship("Location", back_populates="weather_records")

    api_source = Column(String, nullable=True)
    raw_response = Column(JSON, nullable=True)
    tip = Column(String, nullable=True)


# Index Example (for composite indexes, etc.)
Index(
    "ix_weather_location_date", WeatherHistory.location_id, WeatherHistory.weather_date
)
