from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.models import WeatherHistory
from app.schemas.weather import WeatherHistoryCreate, WeatherHistoryUpdate


def create_weather_record(db: Session, data: WeatherHistoryCreate) -> WeatherHistory:
    """
    Create a new weather record.
    """
    db_weather = WeatherHistory(**data.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


def get_weather_by_id(db: Session, weather_id: int) -> Optional[WeatherHistory]:
    """
    Get a weather record by ID.
    """
    return db.query(WeatherHistory).filter(WeatherHistory.id == weather_id).first()


def get_weather_by_location(
    db: Session,
    location_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[WeatherHistory]:
    """
    Get weather records by location ID.
    You can specify the date range.
    """
    query = db.query(WeatherHistory).filter(WeatherHistory.location_id == location_id)

    if start_date:
        query = query.filter(WeatherHistory.weather_date >= start_date)
    if end_date:
        query = query.filter(WeatherHistory.weather_date <= end_date)

    return query.order_by(WeatherHistory.weather_date.desc()).all()


def update_weather_record(
    db: Session, weather_id: int, data: WeatherHistoryUpdate
) -> Optional[WeatherHistory]:
    """
    Update a weather record.
    """
    db_weather = get_weather_by_id(db, weather_id)
    if not db_weather:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_weather, key, value)

    db.commit()
    db.refresh(db_weather)
    return db_weather


def delete_weather_record(db: Session, weather_id: int) -> bool:
    """
    Delete a weather record.
    """
    db_weather = get_weather_by_id(db, weather_id)
    if not db_weather:
        return False

    db.delete(db_weather)
    db.commit()
    return True


def get_forecast(
    db: Session,
    location_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[WeatherHistory]:
    """
    Get weather forecast by location ID.
    You can specify the date range.
    """
    query = db.query(WeatherHistory).filter(WeatherHistory.location_id == location_id)

    if start_date:
        query = query.filter(WeatherHistory.weather_date >= start_date)
    if end_date:
        query = query.filter(WeatherHistory.weather_date <= end_date)

    return query.order_by(WeatherHistory.weather_date.asc()).all()
