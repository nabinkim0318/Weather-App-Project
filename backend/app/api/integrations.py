"""
Module: api.integrations
------------------------

This optional module handles integration with third-party services to enrich the Weather App functionality. It provides
FastAPI endpoints for fetching and serving supplementary content such as YouTube videos and map data related to user locations.

Endpoints:
- GET /api/integrations/youtube
    Retrieves relevant YouTube videos based on the user’s location or weather context (e.g., local weather news, city tours).
- GET /api/integrations/map
    Provides map-related data or embeds for the specified location, supporting multiple map providers.
- Additional endpoints may support traffic data, local alerts, or other location-specific integrations.

Key Responsibilities:
- Validate incoming requests for location and query parameters.
- Communicate with external APIs such as YouTube Data API and Google Maps API to fetch relevant content.
- Handle API key management, rate limiting, and error handling for external service calls.
- Process and format responses to suit frontend display requirements.
- Cache frequent queries to reduce latency and API usage costs.
- Gracefully degrade functionality when external services are unavailable.

Integration Points:
- External APIs (YouTube Data API, Google Maps API, OpenStreetMap, etc.)
- Configuration management for API keys and secrets.
- Cache layers or CDN for performance optimization.
- User authentication for personalized content where applicable.

This module extends the Weather App by embedding rich multimedia and geographic content, increasing user engagement and providing contextual information beyond raw weather data.
"""

from app.services.weather_service import fetch_current_weather, fetch_forecast
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import httpx
import os
import asyncio

router = APIRouter()

# Load API keys from environment variables or configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Simple cache example (Redis recommended in production)
_cache = {}

def build_cache_key(prefix: str, **kwargs) -> str:
    return prefix + ":" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))

async def fetch_youtube_videos(query: str, max_results: int = 5) -> List[dict]:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
        "type": "video",
        "regionCode": "US",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        videos = []
        for item in data.get("items", []):
            videos.append({
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
            })
        return videos

@router.get("/integrations/youtube")
async def get_youtube_videos(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    max_results: int = Query(5, ge=1, le=20),
):
    if not (city or (lat is not None and lon is not None)):
        raise HTTPException(status_code=400, detail="Provide city or lat/lon coordinates.")

    query = city or f"{lat},{lon} weather news"
    cache_key = build_cache_key("youtube", query=query, max_results=max_results)
    cached = _cache.get(cache_key)
    if cached:
        return cached

    try:
        videos = await fetch_youtube_videos(query, max_results)
        _cache[cache_key] = videos
        return videos
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch YouTube videos: {str(e)}")

async def fetch_map_embed(lat: float, lon: float, zoom: int = 12) -> dict:
    # Example: Google Maps Embed API URL
    embed_url = f"https://www.google.com/maps/embed/v1/view?key={GOOGLE_MAPS_API_KEY}&center={lat},{lon}&zoom={zoom}"
    return {"embed_url": embed_url}

@router.get("/integrations/map")
async def get_map_embed(
    lat: float = Query(...),
    lon: float = Query(...),
    zoom: int = Query(12, ge=1, le=20)
):
    cache_key = build_cache_key("map", lat=lat, lon=lon, zoom=zoom)
    cached = _cache.get(cache_key)
    if cached:
        return cached

    try:
        embed_data = await fetch_map_embed(lat, lon, zoom)
        _cache[cache_key] = embed_data
        return embed_data
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch map data: {str(e)}")
