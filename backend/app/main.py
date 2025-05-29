import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app import models
from app.api import export, integrations, search_location, weather
from app.db.database import Base, engine

# from app.models.export import ExportHistory
from app.utils.errors import register_exception_handlers

# from app.models import user, user_location
# from app.services import user_location as svc


load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)

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
)

# --- Register Global Exception Handlers ---
register_exception_handlers(app)

# --- CORS Settings ---
origins = [
    "http://localhost",
    "http://localhost:3000",  # React dev Server Address
]

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


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather App API"}
