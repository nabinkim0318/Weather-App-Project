from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_database_url

# Get database URL from config (respects DATABASE_URL env var)
DATABASE_URL = get_database_url()

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Function to create and manage database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
