"""
Module: models.location
-----------------------

This module defines the ORM (Object-Relational Mapping) model for the Location entity
within the database schema. Using an ORM framework such as SQLAlchemy, this model maps
location-related data to a relational database table, enabling efficient and structured
storage, retrieval, and management of location information used by the application.

Key Responsibilities:
- Define the database schema for the Location table, including columns for key attributes:
  - Unique location identifier (primary key)
  - Human-readable location name (e.g., city, town, landmark)
  - Geographical coordinates (latitude and longitude)
  - Country, state/province information for hierarchical queries
  - Any additional metadata useful for geocoding, fuzzy matching, or caching
- Enforce constraints such as unique indexes on location name or coordinates to prevent
  duplicates.
- Define relationships to other tables/entities such as Users, Weather data, or search
  history to support linked queries and referential integrity.
- Support data validation at the ORM level if applicable, ensuring data consistency.
- Facilitate location-based queries, updates, and deletions from the application layer.
- Enable integration with external geocoding APIs by storing normalized or canonical
  location identifiers.

Usage:
- Utilize the Location model in CRUD operations where locations are created, read,
  updated, or deleted.
- Leverage relationships to join weather data or user preferences associated with a
  particular location.
- Use as part of location search features with fuzzy matching or caching of popular
  locations.

Benefits:
- Provides a centralized, structured representation of location data.
- Enhances query efficiency and data integrity through proper indexing and constraints.
- Simplifies integration with external location-based services.
- Enables extensible design for future location-related features.

Example:
```python
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)

    # Relationships
    users = relationship("User", back_populates="locations")
    weather_records = relationship("WeatherHistory", back_populates="location")
"""