from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal
from app.models.models import SearchLocation


def create_test_data():
    db = SessionLocal()
    try:
        # Create test location data
        locations = [
            SearchLocation(
                label="Busan",
                city="Busan",
                state=None,
                country="KR",
                postal_code="00001",
                latitude=35.1796,
                longitude=129.0756,
            ),
            SearchLocation(
                label="Jeju",
                city="Jeju",
                state=None,
                country="KR",
                postal_code="00002",
                latitude=33.4996,
                longitude=126.5312,
            ),
        ]

        for location in locations:
            try:
                db.add(location)
                db.commit()
                print(f"Added location: {location.city}")
            except SQLAlchemyError as e:
                print(f"Error adding {location.city}: {str(e)}")
                db.rollback()

        # Print all locations
        created_locations = db.query(SearchLocation).all()
        print("\nAll Locations:")
        for loc in created_locations:
            print(f"ID: {loc.id}, City: {loc.city}, Label: {loc.label}")

    except SQLAlchemyError as e:
        print(f"Error accessing database: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
