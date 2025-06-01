import logging
import os

# Load .env file safely
from pathlib import Path as FilePath

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import export, integrations, search_location, weather, weather_history
from app.core.database import Base, engine
from app.utils.errors import register_exception_handlers

# TODO: Integrate user-related services


try:
    env_path = FilePath(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
except Exception as e:
    logging.warning(f"Could not load .env file: {e}")

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# --- Create DB Tables ---
Base.metadata.create_all(bind=engine)

# --- Create FastAPI App ---
app = FastAPI(
    title="Weather App API",
    description=(
        "API for Weather App with CRUD, external API integration, "
        "and export features"
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Weather", "description": "Endpoints for weather data and forecasts"},
        {"name": "Location", "description": "Location search and aliases"},
        {"name": "Export", "description": "Export weather data in various formats"},
        {
            "name": "Integrations",
            "description": "3rd-party integrations like maps, YouTube",
        },
    ],
)

# --- Register Global Exception Handlers ---
register_exception_handlers(app)

# --- CORS Settings ---
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost,http://localhost:3000").split(
    ","
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register API Routers ---
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(search_location.router, prefix="/api/location", tags=["Location"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(
    integrations.router, prefix="/api/integrations", tags=["Integrations"]
)
app.include_router(
    weather_history.router, prefix="/api/weather-history", tags=["Weather History"]
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather App API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
