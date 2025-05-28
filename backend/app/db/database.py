"""
Module: db.database
-------------------

This module is responsible for setting up and managing the database connection and session lifecycle for the application.
It encapsulates the configuration and initialization of the database engine, session creation, and provides utilities for
dependency injection in FastAPI routes.

Key Responsibilities:
- Configure the database connection string (PostgreSQL, MySQL, etc.) and initialize the SQLAlchemy engine.
- Create a thread-safe sessionmaker instance to generate database sessions.
- Provide FastAPI-compatible dependency functions to yield database sessions for request handlers,
  ensuring proper opening and closing of sessions to prevent resource leaks.
- Support asynchronous or synchronous database operations as per project setup.
- Handle connection pooling and engine configuration options such as echo/logging, pool size, and timeout.
- Centralize database setup to ease maintenance and potential database backend changes.
- Facilitate integration with Alembic or other migration tools by providing engine and metadata access.

Typical Usage:
- Import the `get_db` dependency in API route functions to access a transactional DB session.
- Use the session for ORM operations: querying, inserting, updating, and deleting records.
- Ensure sessions are closed automatically after each request to maintain connection pool health.

Integration Points:
- SQLAlchemy ORM and core components.
- Database URL and credentials managed via environment variables or configuration files.
- Migration tooling (Alembic) for schema versioning.
- Logging framework for database query monitoring and debugging.

This module is foundational for data persistence and plays a critical role in ensuring efficient, safe, and consistent
database interactions throughout the application lifecycle.
"""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Load the database URL from environment variable or config
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./test.db"
)  # Replace with production URL as needed

# SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,  # Set to True for SQL echo/debugging
)

# SessionLocal factory for creating new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


# Dependency injection function for FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: context manager for use outside FastAPI (e.g., scripts)
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
