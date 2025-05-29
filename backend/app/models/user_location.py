from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String

# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class UserLocation(Base):
    __tablename__ = "user_locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    label = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    _is_favorite = Column("is_favorite", Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="locations")

    # @hybrid_property
    # def is_favorite(self) -> bool:
    #     return bool(getattr(self, '_is_favorite', False))

    # @is_favorite.setter
    # def is_favorite(self, value: bool) -> None:
    #     self._is_favorite = value
