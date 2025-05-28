# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import weather, location, export, integrations
from app.utils.errors import register_exception_handlers

# Import SQLAlchemy base and model
from app.db.database import Base, engine
from app.models.export import ExportHistory  # Needed for table registration

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather App API",
    description="API for Weather App with CRUD, external API integration, and export features",
    version="1.0.0",
)

# CORS Settings 
origins = [
    "http://localhost",
    "http://localhost:3000",  # React dev Server Address
    # Add domain if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(location.router, prefix="/api/location", tags=["Location"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"])

# Register global exception handlers
register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather App API"}
