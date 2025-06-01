from datetime import datetime

from pydantic import BaseModel


class WeatherHistoryBase(BaseModel):
    location: str
    date: datetime
    temperature: float
    condition: str
    humidity: int
    wind_speed: float


class WeatherHistoryCreate(WeatherHistoryBase):
    pass


class WeatherHistory(WeatherHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WeatherHistorySearch(BaseModel):
    location: str
    start_date: datetime
    end_date: datetime
