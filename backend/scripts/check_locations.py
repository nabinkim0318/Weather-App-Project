from app.core.database import SessionLocal
from app.models.models import SearchLocation


def check_locations():
    db = SessionLocal()
    try:
        locations = db.query(SearchLocation).all()
        print("\nExisting Locations:")
        for loc in locations:
            print(
                f"ID: {loc.id}, City: {loc.city}, Label: {loc.label}, Coords: ({loc.latitude}, {loc.longitude})"
            )
    finally:
        db.close()


if __name__ == "__main__":
    check_locations()
