import os
import sys
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_database_url
from app.models.models import WeatherHistory


def create_test_weather_records():
    # Set up database connection
    SQLALCHEMY_DATABASE_URL = get_database_url()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        # Weather records for Seoul (ID: 1) from March 1 to 7
        seoul_records = [
            {
                "location_id": 1,
                "weather_date": datetime(2024, 3, 1) + timedelta(days=i),
                "temp_c": 15.5 + i,
                "temp_f": (15.5 + i) * 9 / 5 + 32,
                "condition": "Clear" if i % 2 == 0 else "Clouds",
                "humidity": 60 + i,
                "wind_speed": 3.0 + (i * 0.5),
                "condition_desc": "Clear weather" if i % 2 == 0 else "Cloudy weather",
                "icon": "01d" if i % 2 == 0 else "04d",
            }
            for i in range(7)
        ]

        # Weather records for Busan (ID: 3) from March 1 to 7
        busan_records = [
            {
                "location_id": 3,
                "weather_date": datetime(2024, 3, 1) + timedelta(days=i),
                "temp_c": 17.5 + i,
                "temp_f": (17.5 + i) * 9 / 5 + 32,
                "condition": (
                    "Clear" if i % 3 == 0 else "Rain" if i % 3 == 1 else "Clouds"
                ),
                "humidity": 65 + i,
                "wind_speed": 4.0 + (i * 0.5),
                "condition_desc": (
                    "Clear weather"
                    if i % 3 == 0
                    else "Rain" if i % 3 == 1 else "Cloudy weather"
                ),
                "icon": "01d" if i % 3 == 0 else "10d" if i % 3 == 1 else "04d",
            }
            for i in range(7)
        ]

        # Weather records for Jeju (ID: 4) from March 1 to 7
        jeju_records = [
            {
                "location_id": 4,
                "weather_date": datetime(2024, 3, 1) + timedelta(days=i),
                "temp_c": 16.5 + i,
                "temp_f": (16.5 + i) * 9 / 5 + 32,
                "condition": (
                    "Clear"
                    if i % 4 == 0
                    else "Rain" if i % 4 == 1 else "Clouds" if i % 4 == 2 else "Fog"
                ),
                "humidity": 70 + i,
                "wind_speed": 5.0 + (i * 0.5),
                "condition_desc": (
                    "Clear weather"
                    if i % 4 == 0
                    else (
                        "Rain"
                        if i % 4 == 1
                        else "Cloudy weather" if i % 4 == 2 else "Foggy weather"
                    )
                ),
                "icon": (
                    "01d"
                    if i % 4 == 0
                    else "10d" if i % 4 == 1 else "04d" if i % 4 == 2 else "50d"
                ),
            }
            for i in range(7)
        ]

        all_records = seoul_records + busan_records + jeju_records

        # Add records to the database
        for record_data in all_records:
            record = WeatherHistory(**record_data)
            try:
                db.add(record)
                db.commit()
                print(
                    f"Added weather record for {record_data['condition']} at {record_data['weather_date']}"
                )
            except SQLAlchemyError as e:
                print(f"Error adding record: {str(e)}")
                db.rollback()

        print("\nAll test weather records have been created!")

        # Check the created records
        for location_id in [1, 3, 4]:
            records = (
                db.query(WeatherHistory)
                .filter(WeatherHistory.location_id == location_id)
                .order_by(WeatherHistory.weather_date)
                .all()
            )

            print(f"\nRecords for location_id {location_id}:")
            for record in records:
                print(
                    f"Date: {record.weather_date.strftime('%Y-%m-%d')}, "
                    f"Temp: {record.temp_c}°C, "
                    f"Condition: {record.condition}"
                )

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_weather_records()
