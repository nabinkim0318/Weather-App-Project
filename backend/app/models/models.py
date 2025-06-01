"""
데이터베이스 모델 정의
"""

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class SearchLocation(Base):
    __tablename__ = "search_locations"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=True)  # Custom label
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Unique constraint for location coordinates
    __table_args__ = (
        Index("ix_location_coords", "latitude", "longitude", unique=True),
        Index("ix_location_name", "city", "state", "country", unique=True),
    )

    # Define relationships
    weather_records = relationship(
        "WeatherHistory", back_populates="location", lazy="dynamic"
    )
    forecast_records = relationship(
        "WeatherForecast", back_populates="location", lazy="dynamic"
    )

    def __repr__(self):
        return (
            f"<SearchLocation(city={self.city}, lat={self.latitude}, "
            f"lon={self.longitude})>"
        )


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(
        Integer,
        ForeignKey("search_locations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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

    api_source = Column(String, nullable=True)
    raw_response = Column(JSON, nullable=True)
    tip = Column(String, nullable=True)

    # Define relationship
    location = relationship("SearchLocation", back_populates="weather_records")


class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(
        Integer,
        ForeignKey("search_locations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    weather_date = Column(DateTime, nullable=False, index=True)

    temp_min_c = Column(Float, nullable=True)
    temp_max_c = Column(Float, nullable=True)
    condition = Column(String, nullable=True)
    icon = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Define relationship
    location = relationship("SearchLocation", back_populates="forecast_records")
