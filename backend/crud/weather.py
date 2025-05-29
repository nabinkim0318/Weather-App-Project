from datetime import date
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.search_history import SearchHistory
from app.models.search_location import SearchLocation
from app.models.weather import WeatherForecast, WeatherHistory
from app.schemas.weather import WeatherCreate, WeatherUpdate

# ----------------------
# Weather CRUD Functions
# ----------------------


def create_weather_record(db: Session, data: WeatherCreate) -> WeatherHistory:
    weather = WeatherHistory(**data.dict())
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather


def get_weather_by_id(db: Session, weather_id: int) -> Optional[WeatherHistory]:
    return db.query(WeatherHistory).filter(WeatherHistory.id == weather_id).first()


def get_weather_by_location(
    db: Session,
    location_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[WeatherHistory]:
    query = db.query(WeatherHistory).filter(WeatherHistory.location_id == location_id)
    if start_date:
        query = query.filter(WeatherHistory.weather_date >= start_date)
    if end_date:
        query = query.filter(WeatherHistory.weather_date <= end_date)
    return query.order_by(WeatherHistory.weather_date.desc()).all()


def update_weather_record(
    db: Session, weather_id: int, data: WeatherUpdate
) -> Optional[WeatherHistory]:
    weather = get_weather_by_id(db, weather_id)
    if not weather:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(weather, field, value)
    db.commit()
    db.refresh(weather)
    return weather


def delete_weather_record(db: Session, weather_id: int) -> bool:
    weather = get_weather_by_id(db, weather_id)
    if not weather:
        return False
    db.delete(weather)
    db.commit()
    return True


def get_forecast(
    db: Session,
    location_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[WeatherForecast]:
    query = db.query(WeatherForecast).filter(WeatherForecast.location_id == location_id)
    if start_date:
        query = query.filter(WeatherForecast.weather_date >= start_date)
    if end_date:
        query = query.filter(WeatherForecast.weather_date <= end_date)
    return query.order_by(WeatherForecast.weather_date.asc()).all()


# ----------------------
# Location & History
# ----------------------


def get_saved_locations(db: Session, user_id: int) -> List[SearchLocation]:
    return db.query(SearchLocation).filter(SearchLocation.user_id == user_id).all()


def add_search_history(db: Session, user_id: int, query: str):
    record = SearchHistory(user_id=user_id, query=query)
    db.add(record)
    db.commit()


def get_search_history(db: Session, user_id: int) -> List[SearchHistory]:
    return (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == user_id)
        .order_by(SearchHistory.searched_at.desc())
        .all()
    )


def update_saved_location_alias(
    db: Session, location_id: int, alias: str
) -> Optional[SearchLocation]:
    location = db.query(SearchLocation).filter(SearchLocation.id == location_id).first()
    if not location:
        return None
    location.label = alias  # type: ignore[attr-defined]
    db.commit()
    db.refresh(location)
    return location


def clear_search_history(db: Session, user_id: int):
    db.query(SearchHistory).filter(SearchHistory.user_id == user_id).delete()
    db.commit()
