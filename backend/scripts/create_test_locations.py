import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_database_url
from app.models.models import SearchLocation


def create_test_locations():
    # Set up database connection
    SQLALCHEMY_DATABASE_URL = get_database_url()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        # Test location data
        locations = [
            {
                "city": "Seoul",
                "state": "Seoul",
                "country": "South Korea",
                "latitude": 37.5665,
                "longitude": 126.9780,
            },
            {
                "city": "Busan",
                "state": "Busan",
                "country": "South Korea",
                "latitude": 35.1796,
                "longitude": 129.0756,
            },
            {
                "city": "Jeju",
                "state": "Jeju",
                "country": "South Korea",
                "latitude": 33.4996,
                "longitude": 126.5312,
            },
        ]

        # Add locations to the database
        for location_data in locations:
            location = SearchLocation(**location_data)
            try:
                db.add(location)
                db.commit()
                print(
                    f"Added location: {location_data['city']}, {location_data['country']}"
                )
            except SQLAlchemyError as e:
                print(f"Error adding location: {str(e)}")
                db.rollback()

        print("\nAll test locations have been created!")

        # Check the created locations
        locations = db.query(SearchLocation).all()
        print("\nCreated locations:")
        for location in locations:
            print(
                f"ID: {location.id}, City: {location.city}, "
                f"Country: {location.country}, "
                f"Coordinates: ({location.latitude}, {location.longitude})"
            )

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_locations()
