from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/weather")
async def get_weather(city: str = Query(...)):
    return {"message": f"You asked for weather in {city}!"}
