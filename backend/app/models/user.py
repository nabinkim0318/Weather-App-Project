"""
Module: models.user
-------------------

This module defines the ORM (Object-Relational Mapping) model for the User entity in the
database. It leverages SQLAlchemy (or the chosen ORM framework) to map the User model to
a relational database table, enabling seamless interaction with user-related data.

Key Responsibilities:
- Define the database schema for the User table, including columns, data types, and
  constraints such as primary keys, unique fields, and foreign keys.
- Represent essential user attributes such as:
  - Unique identifier (e.g., user ID)
  - Authentication credentials (e.g., username, hashed password, email)
  - Profile information (e.g., full name, contact details)
  - User preferences/settings relevant to the application
  - Timestamps for account creation and updates (audit fields)
- Establish relationships to other entities where applicable, for example:
  - One-to-many or many-to-many relations with Locations, Weather data, or User settings
- Include validation rules or ORM-level constraints to ensure data integrity.
- Support serialization/deserialization if integrated with Pydantic schemas.

Usage:
- Import and use the User model in CRUD operations, authentication workflows, and API
  endpoint implementations.
- Extend or customize the model to accommodate additional user-related features or
  fields as needed.

Benefits:
- Provides a structured and centralized representation of user data in the application.
- Simplifies database operations via ORM abstractions.
- Enhances maintainability by decoupling database schema from business logic.
- Facilitates secure and efficient user management and data access.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Example: User and Location have a 1:N relationship
    locations = relationship("Location", back_populates="user")
