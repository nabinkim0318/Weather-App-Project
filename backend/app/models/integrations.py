"""
Module: models.integrations
---------------------------

This module defines ORM models related to third-party API integrations used within the application,
specifically for services like Google Maps, YouTube, and any API key management required for these integrations.

Key Responsibilities:
- Define models to store API keys securely, including metadata about their usage and status.
- Represent integration-specific configurations or data linked to external services (e.g., YouTube channel info, map preferences).
- Track usage limits, expiration, and renewal information for API keys to manage quota and avoid service interruptions.
- Facilitate storing user or system preferences related to third-party integrations.
- Enable audit and debugging by maintaining logs or metadata of integration requests if applicable.

Primary Models:
- APIKey: Stores credentials and metadata for third-party API access.
- YouTubeIntegration: Represents configuration or data related to YouTube API usage.
- MapIntegration: Represents configuration or data related to map services (e.g., Google Maps API).

Usage:
- Use APIKey model to authenticate and authorize external API calls.
- Manage API keys lifecycle: creation, activation, deactivation, expiration.
- Store integration-specific user preferences or settings.
- Support backend logic to select appropriate keys and integration parameters dynamically.
- Facilitate admin monitoring of third-party integration health and usage.

Benefits:
- Centralizes management of API keys and integration data.
- Enhances security by abstracting keys from application logic.
- Supports scalability by managing multiple keys or integration instances.
- Provides flexibility for future integration extensions.

Example:
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)  # e.g., "Google Maps", "YouTube"
    key_value = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # Relationship to track usage logs if implemented
    usage_logs = relationship("APIKeyUsageLog", back_populates="api_key")

class YouTubeIntegration(Base):
    __tablename__ = "youtube_integrations"

    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    channel_id = Column(String, nullable=True)
    preferences = Column(String, nullable=True)  # JSON or stringified config

    api_key = relationship("APIKey")

class MapIntegration(Base):
    __tablename__ = "map_integrations"

    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
    map_type = Column(String, nullable=True)  # e.g., "Google Maps", "OpenStreetMap"
    preferences = Column(String, nullable=True)  # Configurations or settings

    api_key = relationship("APIKey")
"""
