import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.get("/api/location/weather")
async def get_weather(user_input: str):
    """Get current weather for a location"""
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")
    
    try:
        # Determine if input is coordinates
        if "," in user_input and len(user_input.split(",")) == 2:
            lat, lon = user_input.split(",")
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        else:
            # Treat as city name or zip code
            url = f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={OPENWEATHER_API_KEY}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 404:
                raise HTTPException(status_code=400, detail=f"Location '{user_input}' not found")
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")

@app.get("/api/weather/forecast")
async def get_forecast(city: str):
    """Get 5-day forecast for a city"""
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 404:
                raise HTTPException(status_code=400, detail=f"City '{city}' not found")
            response.raise_for_status()
            data = response.json()
            
            # Transform to match expected format
            forecast_data = {
                "location": {
                    "city": data["city"]["name"],
                    "country": data["city"]["country"],
                    "latitude": data["city"]["coord"]["lat"],
                    "longitude": data["city"]["coord"]["lon"]
                },
                "forecast": []
            }
            
            for item in data["list"]:
                forecast_item = {
                    "forecast_date": item["dt_txt"].split(" ")[0],
                    "forecast_hour": int(item["dt_txt"].split(" ")[1].split(":")[0]),
                    "temp_c": round(item["main"]["temp"] - 273.15, 1),
                    "temp_f": round((item["main"]["temp"] - 273.15) * 9/5 + 32, 1),
                    "condition": item["weather"][0]["main"],
                    "condition_desc": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"],
                    "icon_url": f"https://openweathermap.org/img/w/{item['weather'][0]['icon']}.png"
                }
                forecast_data["forecast"].append(forecast_item)
            
            return forecast_data
            
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast data")

@app.get("/api/weather/hourly")
async def get_hourly_weather(city: str):
    """Get hourly weather forecast"""
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 404:
                raise HTTPException(status_code=400, detail=f"City '{city}' not found")
            response.raise_for_status()
            data = response.json()
            
            hourly_data = {
                "location": data["city"]["name"],
                "hourly_forecast": []
            }
            
            for item in data["list"][:24]:  # Next 24 hours
                hourly_item = {
                    "hour": item["dt_txt"].split(" ")[1][:5],
                    "timestamp": item["dt"],
                    "temperature": round(item["main"]["temp"] - 273.15, 1),
                    "condition": item["weather"][0]["main"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                }
                hourly_data["hourly_forecast"].append(hourly_item)
            
            return hourly_data
            
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail="Failed to fetch hourly data")

@app.get("/api/integrations/youtube")
async def get_youtube_videos(city: str):
    """Get travel-related YouTube videos"""
    if not YOUTUBE_API_KEY:
        return []  # Return empty array if no API key
    
    try:
        categories = {
            "weather": f"{city} weather forecast today",
            "restaurants": f"top 10 best restaurants in {city} food guide", 
            "weekend": f"Fun things to do in {city}"
        }
        
        all_videos = []
        
        async with httpx.AsyncClient() as client:
            for category, query in categories.items():
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": 1,
                    "key": YOUTUBE_API_KEY,
                    "order": "relevance"
                }
                
                try:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    for item in data.get("items", []):
                        video_id = item["id"]["videoId"]
                        video = {
                            "videoId": video_id,
                            "title": item["snippet"]["title"],
                            "description": item["snippet"]["description"],
                            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                            "embed_url": f"https://www.youtube.com/embed/{video_id}",
                            "watch_url": f"https://www.youtube.com/watch?v={video_id}",
                            "category": category
                        }
                        all_videos.append(video)
                except:
                    continue  # Skip failed requests
        
        return all_videos
        
    except:
        return []  # Return empty array on any error

@app.get("/")
async def root():
    return {"message": "Weather API is running"}

# This is required for Vercel
handler = app 