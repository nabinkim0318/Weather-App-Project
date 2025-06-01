"""
Module: core.config
------------------

This module manages application configuration settings, including API keys,
database connections, and other environment-specific variables.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    openweather_api_key: Optional[str] = None
    youtube_api_key: Optional[str] = None
    google_maps_api_key: Optional[str] = None

    # API URLs
    openweather_api_url: str = "https://api.openweathermap.org/data/2.5"
    youtube_api_url: str = "https://www.googleapis.com/youtube/v3"

    # Database settings
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "weather_app"

    database_url: Optional[str] = None

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings instance"""
    return Settings()


settings = get_settings()


def get_database_url() -> str:
    """Get the database URL."""
    if settings.database_url:
        return settings.database_url
    return (
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )
