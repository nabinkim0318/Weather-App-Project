"""
Module: api.export
------------------

This module provides FastAPI endpoints for exporting weather and related data into various file formats, enabling users to
download or share their data conveniently. It supports common export formats including CSV, JSON, and PDF.

Endpoints:
- GET /api/export/csv
    Exports weather data (current, forecast, or history) as a CSV file.
- GET /api/export/json
    Exports weather data in JSON format with optional pretty-printing.
- GET /api/export/pdf
    Generates a PDF report of weather data, including charts and summaries.
- Additional endpoints may support filtering exported data by location, date range, or user preferences.

Key Responsibilities:
- Validate export request parameters including data scope, format, and filters.
- Fetch the relevant data from the database or cache for export.
- Format data appropriately for each export type:
    - CSV: tabular data with correct headers and encoding.
    - JSON: structured and optionally human-readable JSON.
    - PDF: well-designed report including text, images, and charts.
- Handle large data exports efficiently to avoid blocking and memory overload.
- Stream file responses with proper HTTP headers for download.
- Manage error handling for invalid parameters, data retrieval failures, or export generation issues.
- Optionally log export activity for auditing or usage metrics.

Integration Points:
- Database for retrieving stored weather and user data.
- PDF generation libraries (e.g., ReportLab, WeasyPrint, or wkhtmltopdf).
- CSV and JSON serialization utilities.
- Authentication and authorization middleware to ensure data privacy.

This module enhances user experience by providing flexible, reliable data export capabilities crucial for reporting, analysis, and sharing.

Additional Enhancements:
- Error Handling:
    - Returns HTTP 404 for missing or empty data sets.
    - Catches unexpected errors and responds with HTTP 500 and descriptive messages.
- PDF Export:
    - Uses ReportLab to dynamically generate summary-style PDF documents.
    - PDF content includes formatted weather data and may be extended with charts or styled layouts.
"""
from fastapi import APIRouter, Query, HTTPException, Response, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.database import get_db
from app.services import export_service
from app.schemas.export import ExportHistoryRead, ExportHistoryCreate, ExportHistoryUpdate
from app.models.export import ExportHistory
from sqlalchemy import select

import io

router = APIRouter(tags=["Export"])

# Mock weather data (replace with DB logic later)
mock_data = [
    {"date": "2025-05-27", "location": "New York", "temperature": 22, "condition": "Sunny"},
    {"date": "2025-05-28", "location": "New York", "temperature": 24, "condition": "Cloudy"}
]

def get_data() -> list:
    if not mock_data:
        raise HTTPException(status_code=404, detail="No data available for export.")
    return mock_data


def log_export(db: Session, export_type: str, status: str = "success", error: Optional[str] = None):
    entry = ExportHistoryCreate(
        export_type=export_type,
        export_params={"source": "mock"},
        user_id=None
    )
    data = entry.dict()
    data.pop("user_id", None)  

    export_record = ExportHistory(**data, status=status, error_message=error)
    print("Logging export:", export_record)  
    db.add(export_record)
    db.commit()


@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    try:
        data = get_data()
        buffer = export_service.export_to_csv(data)
        log_export(db, export_type="csv")
        return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=weather_data.csv"
        })
    except Exception as e:
        log_export(db, export_type="csv", status="failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")


@router.get("/json")
def export_json(pretty: Optional[bool] = Query(False), db: Session = Depends(get_db)):
    try:
        data = get_data()
        json_data = export_service.export_to_json(data, pretty=pretty or False)
        log_export(db, export_type="json")
        return Response(content=json_data, media_type="application/json", headers={
            "Content-Disposition": "attachment; filename=weather_data.json"
        })
    except Exception as e:
        log_export(db, export_type="json", status="failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"JSON export failed: {str(e)}")


@router.get("/pdf")
def export_pdf(db: Session = Depends(get_db)):
    try:
        data = get_data()
        buffer = export_service.export_to_pdf(data)
        log_export(db, export_type="pdf")
        return StreamingResponse(buffer, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=weather_report.pdf"
        })
    except Exception as e:
        log_export(db, export_type="pdf", status="failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")
    
@router.get("/history", response_model=List[ExportHistoryRead])
def get_export_history(
    export_type: Optional[str] = None,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve export history logs with optional filtering.
    """
    query = select(ExportHistory)

    if export_type:
        query = query.where(ExportHistory.export_type == export_type)
    if status:
        query = query.where(ExportHistory.status == status)
    if user_id:
        query = query.where(ExportHistory.user_id == user_id)

    results = db.execute(query).scalars().all()
    return results