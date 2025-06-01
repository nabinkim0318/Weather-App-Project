"""
Module: api.integrations
------------------------

This optional module handles integration with third-party services to enrich
the Weather App functionality. It provides FastAPI endpoints for fetching and
serving supplementary content such as YouTube videos and map data related to
user locations.

Endpoints:
- GET /api/integrations/youtube
    Retrieves relevant YouTube videos based on the user's location or weather
    context (e.g., local weather news, city tours).
- GET /api/integrations/map
    Provides map-related data or embeds for the specified location, supporting
    multiple map providers.
- Additional endpoints may support traffic data, local alerts, or other
  location-specific integrations.

Key Responsibilities:
- Validate incoming requests for location and query parameters.
- Communicate with external APIs such as YouTube Data API and Google
  Maps API to fetch relevant content.
- Handle API key management, rate limiting, and error handling for external
  service calls.
- Process and format responses to suit frontend display requirements.
- Cache frequent queries to reduce latency and API usage costs.
- Gracefully degrade functionality when external services are unavailable.

Integration Points:
- External APIs (YouTube Data API, Google Maps API, OpenStreetMap, etc.)
- Configuration management for API keys and secrets.
- Cache layers or CDN for performance optimization.
- User authentication for personalized content where applicable.

This module extends the Weather App by embedding rich multimedia and geographic
content, increasing user engagement and providing contextual information beyond
raw weather data.
"""

# import asyncio
import os
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

# from app.services.weather_service import fetch_current_weather, fetch_forecast

router = APIRouter()

# Load API keys from environment variables or configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Simple cache example (Redis recommended in production)
_cache = {}


def build_cache_key(prefix: str, **kwargs) -> str:
    return prefix + ":" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))


# YouTube Videos
async def fetch_youtube_videos_by_category(city: str, category: str, max_results=1):
    """
    Fetch YouTube videos based on city and category
    Categories: weather, restaurants, weekend
    """
    queries = {
        "weather": f"{city} weather forecast today",
        "restaurants": f"top 10 best restaurants in {city} food guide",
        "weekend": f"Fun things to do in {city} ",
    }

    query = queries.get(category, f"{city} travel guide")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": os.environ.get("YOUTUBE_API_KEY"),
        "order": "relevance",
        "publishedAfter": "2023-01-01T00:00:00Z",  # Get relatively recent videos
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        videos = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            videos.append(
                {
                    "videoId": video_id,
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                    "embed_url": f"https://www.youtube.com/embed/{video_id}",
                    "watch_url": f"https://www.youtube.com/watch?v={video_id}",
                    "category": category,
                }
            )

        return videos


async def fetch_youtube_videos(query, max_results=3):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": os.environ.get("YOUTUBE_API_KEY"),
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        videos = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            videos.append(
                {
                    "videoId": video_id,
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["high"][
                        "url"
                    ],  # or 'default'
                    "embed_url": f"https://www.youtube.com/embed/{video_id}",
                    "watch_url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )

        return videos


@router.get("/youtube")
async def get_youtube_videos(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    if not (city or (lat is not None and lon is not None)):
        raise HTTPException(
            status_code=400, detail="Provide city or lat/lon coordinates."
        )

    # If lat/lon provided, we need to get city name first (simplified for now)
    location_name = city or "Unknown City"

    cache_key = build_cache_key("youtube_travel", city=location_name)
    cached = _cache.get(cache_key)
    if cached:
        return cached

    try:
        # Fetch videos for all 3 categories
        weather_videos = await fetch_youtube_videos_by_category(
            location_name, "weather", 1
        )
        restaurant_videos = await fetch_youtube_videos_by_category(
            location_name, "restaurants", 1
        )
        weekend_videos = await fetch_youtube_videos_by_category(
            location_name, "weekend", 1
        )

        # Combine all videos
        all_videos = weather_videos + restaurant_videos + weekend_videos

        _cache[cache_key] = all_videos
        return all_videos
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Failed to fetch YouTube videos: {str(e)}"
        )


# Map Embed
async def geocode_location(location: str) -> tuple[float, float]:
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("Missing Google Maps API key")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": api_key}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        if not data["results"]:
            raise ValueError("Location not found")
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]


async def fetch_map_embed(lat: float, lon: float, zoom: int = 12) -> dict:
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    embed_url = (
        f"https://www.google.com/maps/embed/v1/view"
        f"?key={api_key}&center={lat},{lon}&zoom={zoom}"
    )
    return {"embed_url": embed_url}


@router.get("/map")
async def get_map_embed(
    city: Optional[str] = Query(None),
    zip: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    zoom: Optional[int] = Query(12, ge=1, le=20),
):
    if lat is None or lon is None:
        # fallback to geocoding using zip or city
        query = city or zip
        if not query:
            raise HTTPException(status_code=400, detail="Provide lat/lon or city/zip.")
        try:
            lat, lon = await geocode_location(query)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid location: {str(e)}")

    cache_key = build_cache_key("map", lat=lat, lon=lon, zoom=zoom)
    if cache_key in _cache:
        return _cache[cache_key]

    try:
        embed_data = await fetch_map_embed(lat, lon, zoom or 12)
        _cache[cache_key] = embed_data
        return embed_data
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Failed to fetch map data: {str(e)}"
        )
