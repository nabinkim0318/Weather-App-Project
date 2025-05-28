from backend.app.api.search_location import (
    load_openweather_api_key,
    resolve_input_and_fetch_weather,
)

api_key = load_openweather_api_key()
result = resolve_input_and_fetch_weather("Seoul", api_key)

print(result)
