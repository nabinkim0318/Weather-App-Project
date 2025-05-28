"""
Module: schemas.export
----------------------

This module defines Pydantic schemas for validating and serializing data related to export history records.
These schemas are used for API input/output and ensure consistent, structured communication between client and server.

Key Responsibilities:
- Define base and full schemas for ExportHistory model.
- Provide request and response models for export logging, listing, and status feedback.
- Support FastAPI's automatic documentation and data validation.

Usage:
- Use ExportHistoryCreate when creating new export records.
- Use ExportHistoryRead for returning export records in API responses.
- Use ExportHistoryUpdate for patching status or metadata.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ExportHistoryBase(BaseModel):
    export_type: str = Field(default=..., description="Export file type (csv, json, pdf)")
    export_params: Optional[Dict[str, Any]] = Field(None, description="Export parameters")

class ExportHistoryCreate(ExportHistoryBase):
    user_id: Optional[int] = None

class ExportHistoryUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Export status")
    error_message: Optional[str] = None

class ExportHistoryRead(ExportHistoryBase):
    id: int
    user_id: Optional[int] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
