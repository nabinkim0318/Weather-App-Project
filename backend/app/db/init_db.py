# backend/app/db/init_db.py
from app.db.database import Base, engine
from app.models.export import ExportHistory  # Add other models too


def init():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init()
