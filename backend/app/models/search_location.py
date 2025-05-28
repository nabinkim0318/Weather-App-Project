# models/search_location.py

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, func

from app.db.database import Base


class SearchLocation(Base):
    __tablename__ = "search_locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    query = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
