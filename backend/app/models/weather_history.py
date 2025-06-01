from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class WeatherHistory(Base):
    __tablename__ = "weather_history"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    date = Column(DateTime, index=True)
    temperature = Column(Float)
    condition = Column(String)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    created_at = Column(DateTime, default=func.now())
