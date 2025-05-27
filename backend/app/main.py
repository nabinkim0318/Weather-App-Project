from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/weather")
async def get_weather(city: str = Query(...)):
    return {"message": f"You asked for weather in {city}!"}
