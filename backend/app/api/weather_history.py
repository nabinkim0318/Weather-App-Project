"""
# Weather History Management API Endpoints

This module provides endpoints for managing weather history records.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import weather as weather_crud
from app.models.models import SearchLocation
from app.schemas.weather import (
    WeatherBase,
    WeatherHistoryCreate,
    WeatherHistoryResponse,
    WeatherHistoryUpdate,
    WeatherSearchResponse,
    WeatherSearchResult,
)
from app.services.weather_service import (
    fetch_current_weather,
    fetch_forecast,
    fetch_hourly_weather,
    get_weather_tip,
)

router = APIRouter()


async def validate_or_create_location(location_id: int, db: Session):
    """Check if the location ID exists, and if not, create a new location."""
    location = db.query(SearchLocation).filter(SearchLocation.id == location_id).first()
    if not location:
        # Create a new location
        new_location = SearchLocation(
            id=location_id,
            label=f"Location {location_id}",
            city=f"City {location_id}",
            country="Unknown",
            latitude=0.0,  # Default value
            longitude=0.0,  # Default value
        )
        try:
            db.add(new_location)
            db.commit()
            db.refresh(new_location)
            return new_location
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unable to create location ID {location_id}. "
                    "Please use a different ID."
                ),
            )
    return location


async def validate_date_range(
    start_date: Optional[datetime], end_date: Optional[datetime]
):
    """Validate the date range."""
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be before the end date."
        )

    # Past data can only be viewed up to 1 year ago
    if start_date and start_date < datetime.now() - timedelta(days=365):
        raise HTTPException(
            status_code=400, detail="Past data can only be viewed up to 1 year ago."
        )

    # Future data can only be viewed up to 7 days from now
    if end_date and end_date > datetime.now() + timedelta(days=7):
        raise HTTPException(
            status_code=400,
            detail="Future data can only be viewed up to 7 days from now.",
        )


@router.post("/record", response_model=WeatherHistoryResponse)
async def create_weather_record(
    data: WeatherHistoryCreate = Body(
        ...,
        example={
            "location_id": 2,
            "weather_date": "2024-03-20T00:00:00",
            "temp_c": 20.5,
            "temp_f": 68.9,
            "humidity": 65,
            "wind_speed": 5.2,
            "condition": "Clear",
            "condition_desc": "Clear",
            "icon": "01d",
        },
        openapi_examples={
            "Basic Example": {
                "summary": "Basic Weather Record",
                "description": "Basic weather record with only required fields",
                "value": {
                    "location_id": 2,
                    "weather_date": "2024-03-20T00:00:00",
                    "temp_c": 20.5,
                    "temp_f": 68.9,
                    "condition": "Clear",
                },
            },
            "Detailed Example": {
                "summary": "Detailed Weather Record",
                "description": "Detailed weather record with optional fields",
                "value": {
                    "location_id": 2,
                    "weather_date": "2024-03-20T00:00:00",
                    "temp_c": 20.5,
                    "temp_f": 68.9,
                    "condition": "Clear",
                    "condition_desc": "Clear",
                    "humidity": 65,
                    "wind_speed": 5.2,
                    "wind_deg": 180,
                    "icon": "01d",
                },
            },
        },
    ),
    db: Session = Depends(get_db),
):
    """
    Create a new weather record.

    ## Description
    - If the specified location ID does not exist, a new location
    will be automatically created.
    - Location information can be updated later.

    ## Required Fields
    - **location_id**: Location ID (integer)
    - **weather_date**: Weather date (ISO 8601 format)
    - **temp_c**: Celsius temperature (float)
    - **temp_f**: Fahrenheit temperature (float)
    - **condition**: Weather condition (string)

    ## Optional Fields
    - **humidity**: Humidity (0-100)
    - **wind_speed**: Wind speed (m/s)
    - **wind_deg**: Wind direction (0-360)
    - **condition_desc**: Weather condition description (string)
    - **icon**: Weather icon code (string)

    ## Response
    - Success: Created weather record (200 OK)
    - Failure:
        - 400: Bad request (missing required fields or invalid format)
        - 500: Server error

    ## Example Request
    ```json
    {
        "location_id": 2,
        "weather_date": "2024-03-20T00:00:00",
        "temp_c": 20.5,
        "temp_f": 68.9,
        "condition": "Clear",
        "humidity": 65,
        "wind_speed": 5.2,
        "condition_desc": "Clear",
        "icon": "01d"
    }
    ```
    """
    try:
        # Check or create location ID
        # location = await validate_or_create_location(data.location_id, db)

        # If weather_date is a string, convert it to datetime
        if isinstance(data.weather_date, str):
            try:
                # If Z is included, process as UTC time
                weather_date_str = data.weather_date
                if weather_date_str.endswith("Z"):
                    weather_date_str = weather_date_str[:-1] + "+00:00"
                data.weather_date = datetime.fromisoformat(weather_date_str)
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid date format: {str(e)}"
                )

        # Validate date range
        if data.weather_date > datetime.now() + timedelta(days=7):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Future weather records can only be created up to 7 days"
                    "from now."
                ),
            )

        # Validate temperature range
        if data.temp_c < -100 or data.temp_c > 100:
            raise HTTPException(
                status_code=400, detail="Invalid temperature range. (-100°C ~ 100°C)"
            )

        # Validate humidity range
        if data.humidity is not None and (data.humidity < 0 or data.humidity > 100):
            raise HTTPException(
                status_code=400, detail="Invalid humidity range. (0-100%)"
            )

        # Validate wind speed range
        if data.wind_speed is not None and data.wind_speed < 0:
            raise HTTPException(
                status_code=400, detail="Wind speed must be 0 or greater."
            )

        return weather_crud.create_weather_record(db=db, data=data)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating weather record: {str(e)}"
        )


@router.get("/{weather_id}", response_model=WeatherHistoryResponse)
async def get_weather_record(weather_id: int, db: Session = Depends(get_db)):
    """
    Get a weather record by ID.
    """
    try:
        weather = weather_crud.get_weather_by_id(db=db, weather_id=weather_id)
        if not weather:
            raise HTTPException(
                status_code=404, detail=f"Weather record ID {weather_id} not found."
            )
        return weather
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/location/{location_id}", response_model=List[WeatherHistoryResponse])
async def get_location_weather(
    location_id: int,
    start_date: Optional[str] = Query(
        None,
        description="Start date (ISO 8601 format)",
        example="2024-03-04T00:00:00",
        openapi_examples={
            "Basic Example": {
                "summary": "Basic date format",
                "description": "Specify the start date in ISO 8601 format",
                "value": "2024-03-04T00:00:00",
            },
            "Date Only": {
                "summary": "Date only",
                "description": "Specify the date only (automatically set to 00:00:00)",
                "value": "2024-03-04",
            },
            "Timezone Included": {
                "summary": "Timezone included",
                "description": "Date format with timezone",
                "value": "2024-03-04T00:00:00Z",
            },
        },
    ),
    end_date: Optional[str] = Query(
        None,
        description="End date (ISO 8601 format)",
        example="2024-03-05T23:59:59",
        openapi_examples={
            "Basic Example": {
                "summary": "Basic date format",
                "description": "Specify the end date in ISO 8601 format",
                "value": "2024-03-05T23:59:59",
            },
            "Date Only": {
                "summary": "Date only",
                "description": "Specify the date only (automatically set to 23:59:59)",
                "value": "2024-03-05",
            },
            "Timezone Included": {
                "summary": "Timezone included",
                "description": "Date format with timezone",
                "value": "2024-03-05T23:59:59Z",
            },
        },
    ),
    db: Session = Depends(get_db),
):
    """
    Get weather records for a specific location.

    ## Description
    - Get weather records for a specific location.
    - Specify the start and end dates to view records for a specific period.
    - Dates are supported in ISO 8601 format.

    ## Parameters
    - **location_id**: Location ID (integer)
    - **start_date**: Start date (optional)
    - **end_date**: End date (optional)

    ## Response
    - Success: Return weather record list (200 OK)
    - Failure:
        - 404: Location not found
        - 400: Invalid date format or range
        - 500: Server error

    ## Example
    ```
    GET /api/weather-history/location/1?start_date=2024-03-
    04T00:00:00&end_date=
    2024-03-05T23:59:59
    ```

    ## Response Example
    ```json
    [
        {
            "id": 1,
            "location_id": 1,
            "weather_date": "2024-03-04T12:00:00",
            "temp_c": 20.5,
            "temp_f": 68.9,
            "condition": "Clear",
            "humidity": 65,
            "wind_speed": 3.5,
            "created_at": "2024-03-04T12:00:00"
        }
    ]
    ```
    """
    try:
        # Check if the location ID exists
        # location = await validate_or_create_location(location_id, db)

        # Convert date strings to datetime
        start_datetime = None
        end_datetime = None

        if start_date:
            try:
                start_datetime = datetime.fromisoformat(
                    start_date.replace("Z", "+00:00")
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid start date format: {str(e)}"
                )

        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid end date format: {str(e)}"
                )

        # Validate date range
        if start_datetime and end_datetime and start_datetime > end_datetime:
            raise HTTPException(
                status_code=400, detail="Start date must be before the end date."
            )

        # Get weather records
        records = weather_crud.get_weather_by_location(
            db=db,
            location_id=location_id,
            start_date=start_datetime,
            end_date=end_datetime,
        )

        # 응답 데이터 구성
        return records  # ORM 모드를 사용하므로 직접 반환 가능
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting weather records: {str(e)}"
        )


@router.put("/{weather_id}", response_model=WeatherHistoryResponse)
async def update_weather_record(
    weather_id: int, data: WeatherHistoryUpdate, db: Session = Depends(get_db)
):
    """
    Update a specific weather record.
    """
    try:
        # Check if the record exists
        existing_record = weather_crud.get_weather_by_id(db, weather_id)
        if not existing_record:
            raise HTTPException(
                status_code=404, detail=f"Weather record ID {weather_id} not found."
            )

        # Check if the location ID has changed
        if data.location_id and data.location_id != existing_record.location_id:
            await validate_or_create_location(data.location_id, db)

        # Validate date
        if data.weather_date:
            if data.weather_date > datetime.now() + timedelta(days=7):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Future weather records can only be updated up to 7 days"
                        "from now."
                    ),
                )

        # Validate temperature
        if data.temp_c is not None and (data.temp_c < -100 or data.temp_c > 100):
            raise HTTPException(
                status_code=400, detail="Invalid temperature range. (-100°C ~ 100°C)"
            )

        weather = weather_crud.update_weather_record(
            db=db, weather_id=weather_id, data=data
        )
        return weather
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating weather record: {str(e)}"
        )


@router.delete("/{weather_id}")
async def delete_weather_record(weather_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific weather record.
    """
    try:
        # Check if the record exists
        existing_record = weather_crud.get_weather_by_id(db, weather_id)
        if not existing_record:
            raise HTTPException(
                status_code=404, detail=f"Weather record ID {weather_id} not found."
            )

        success = weather_crud.delete_weather_record(db=db, weather_id=weather_id)
        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to delete weather record."
            )
        return {"message": "Weather record deleted successfully."}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting weather record: {str(e)}"
        )


@router.get("/forecast/{location_id}", response_model=List[WeatherHistoryResponse])
async def get_weather_forecast(
    location_id: int,
    start_date: Optional[datetime] = Query(
        None, description="Start date (YYYY-MM-DD HH:MM:SS)"
    ),
    end_date: Optional[datetime] = Query(
        None, description="End date (YYYY-MM-DD HH:MM:SS)"
    ),
    db: Session = Depends(get_db),
):
    """
    Get weather forecast for a specific location.
    You can specify the date range.
    """
    try:
        # Check if the location ID exists
        await validate_or_create_location(location_id, db)

        # Validate date range (forecast is only for future data)
        if start_date and start_date < datetime.now():
            raise HTTPException(
                status_code=400, detail="Start date must be after the current date."
            )

        if end_date and end_date > datetime.now() + timedelta(days=7):
            raise HTTPException(
                status_code=400,
                detail="Forecast is only available up to 7 days from now.",
            )

        return weather_crud.get_forecast(
            db=db, location_id=location_id, start_date=start_date, end_date=end_date
        )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 오류: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting weather forecast: {str(e)}"
        )


@router.get("/search", response_model=WeatherSearchResponse)
async def search_weather(
    query: str = Query(
        ..., description="City name, postal code, or location coordinates"
    ),
    include_forecast: bool = Query(False, description="Include daily forecast"),
    include_hourly: bool = Query(False, description="Include hourly forecast"),
    db: Session = Depends(get_db),
):
    """
    Search for a location and get weather information.

    - Search by city name, postal code, or location coordinates
    - Provide current weather information
    - Optionally include daily/hourly forecast
    - Provide weather tips
    """
    try:
        # Search for current weather
        current = await fetch_current_weather(city=query)
        if not current:
            return WeatherSearchResponse(
                success=False, error="Weather information not found."
            )

        # Create location information
        location = WeatherBase(
            city=getattr(current, "city", None),
            country=getattr(current, "country", None),
            latitude=getattr(current, "latitude", None),
            longitude=getattr(current, "longitude", None),
        )

        # Create search result object
        result = WeatherSearchResult(
            location=location, current_weather=current, last_updated=datetime.now()
        )

        # Get daily forecast (optional)
        if include_forecast:
            forecast = await fetch_forecast(city=query)
            if forecast:
                result.daily_forecast = forecast.forecast

        # Get hourly forecast (optional)
        if include_hourly:
            hourly = await fetch_hourly_weather(city=query)
            if hourly:
                result.hourly_forecast = hourly.hourly_forecast

        # Add weather tip
        result.weather_tip = get_weather_tip(current.condition)

        return WeatherSearchResponse(
            success=True,
            message="Weather information retrieved successfully.",
            result=result,
        )

    except Exception as e:
        return WeatherSearchResponse(
            success=False, error=f"Error getting weather information: {str(e)}"
        )
