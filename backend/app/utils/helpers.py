"""
Module: utils.helpers
---------------------

This module contains a collection of general-purpose utility functions used throughout
the backend application. These helpers assist in common tasks such as data formatting,
conversion, and transformation, improving code reusability and maintainability.

Key Functionalities:
- Data Formatting:
  Functions to format dates, timestamps, temperature units, and other
  domain-specific data into consistent, human-readable strings or
  API-compatible formats.

- API Response Processing:
  Helpers to standardize and sanitize external API responses, extract relevant fields,
  and convert data structures as needed for internal use.

- Conversion Utilities:
  Functions to convert between units (e.g., Celsius to Fahrenheit), data types,
  or encoding schemes that simplify business logic and prevent duplication.

- Serialization Helpers:
  Assist with preparing data for JSON serialization, including handling datetime
  objects, nested models, and optional fields gracefully.

- Miscellaneous Utilities:
  Small helper functions for string manipulations, safe dictionary access, generating
  unique identifiers, and other common coding patterns.

Design Principles:
- Keep each helper function focused and single-purpose to promote
  clarity and testability.
- Avoid side effects; helpers should be pure functions where possible.
- Provide clear, descriptive function names and docstrings for ease of use.
- Optimize for performance when handling frequently used operations.

Usage:
- Import and utilize these helpers in service layers, API routers, or database modules.
- Combine helpers to build more complex transformations or validations as needed.

Benefits:
- Reduces code duplication across the project.
- Enhances code readability by abstracting complex or repetitive tasks.
- Facilitates consistent data formatting and processing standards across modules.
"""


def get_weather_tip(condition: str) -> str:
    tip_map = {
        "Rain": "Bring an umbrella ☔️",
        "Snow": "Wear warm clothes ❄️",
        "Clear": "Perfect day for a walk 🌞",
        "Clouds": "Might be gloomy, stay productive ☁️",
        "Thunderstorm": "Stay indoors and safe ⛈️",
    }
    return tip_map.get(condition, "Stay prepared and check the forecast!")


def icon_url(icon_code: str) -> str:
    return f"/static/icons/{icon_code}.svg"
