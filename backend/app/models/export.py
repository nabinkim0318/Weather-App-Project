"""
Module: models.export
---------------------

This module defines ORM models related to export operations within the application's database.
It enables tracking and management of data exports performed by users, including export types,
timestamps, associated user or session information, and metadata about the exported data.

Key Responsibilities:
- Define a data model representing export history records for audit, analytics, and user support.
- Store information such as:
  - Export ID (primary key)
  - Export type (e.g., CSV, JSON, PDF)
  - Timestamp of export action
  - User or session identifier associated with the export (optional)
  - Parameters or filters used for the export (e.g., date range, location)
  - Status or result of the export operation (success, failure, error message)
- Facilitate querying export history to provide users with a record of their previous exports.
- Enable backend or admin monitoring of export activity and troubleshooting.

Usage:
- Use ExportHistory model to log every export action initiated via API endpoints.
- Reference ExportHistory for displaying export logs in user interfaces or admin dashboards.
- Integrate with export service logic to record export metadata and status updates.
- Support pagination and filtering of export history records in queries.

Benefits:
- Maintains traceability and accountability for data exports.
- Helps detect misuse or excessive export activity.
- Assists in debugging export failures or performance issues.
- Supports compliance with data governance policies.
"""

import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import \
    Base  # Assumes you have a `Base` declared in `database.py`

# from app.models.user import User


class ExportHistory(Base):
    __tablename__ = "export_history"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    export_type = Column(String, nullable=False)  # e.g., "csv", "json", "pdf"
    export_params = Column(
        JSON, nullable=True
    )  # JSON storing filters, date ranges, etc.
    status = Column(
        String, nullable=False, default="pending"
    )  # pending, success, failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # user = relationship("User", back_populates="exports")  # Assumes a related User model
