"""
Module: utils.errors
-------------------

This module defines custom exception classes used across the backend application
to standardize error reporting and handling. It also implements global exception
handlers that translate internal exceptions into appropriate HTTP responses,
providing consistent and meaningful feedback to API clients.

Key Components:
- Custom Exception Classes:
  - ValidationError: Raised when input data fails validation checks.
  - NotFoundError: Raised when requested resources such as locations or weather
    records are not found.
  - DuplicateEntryError: Raised when attempting to create a resource that violates
    uniqueness constraints.
  - ExternalAPIError: Raised for failures related to external API calls.
  - DatabaseError: Raised on database connection or query execution failures.
  - AuthorizationError: Raised when authentication or authorization fails.
  - ConflictError: Raised for concurrency or data conflict issues.
  - SerializationError: Raised during JSON/XML/CSV serialization or deserialization failures.
  - TimeoutError: Raised when operations exceed predefined time limits.

- Global Exception Handlers:
  - Catch exceptions raised within API routes or services.
  - Map exceptions to standard HTTP status codes (e.g., 400, 404, 409, 500).
  - Format error messages into consistent JSON response payloads.
  - Log errors with relevant context for troubleshooting.
  - Handle unexpected exceptions gracefully to avoid leaking sensitive information.

Usage:
- Raise defined exceptions in service and CRUD layers to indicate specific error conditions.
- Register global handlers with FastAPI's exception middleware.
- Enable centralized control over error response formatting and logging.

Benefits:
- Improves API usability by providing clear, standardized error messages.
- Simplifies error handling logic across the codebase.
- Enhances security by controlling exception exposure.
- Facilitates easier debugging and monitoring through structured logs.

This module is a cornerstone for robust backend reliability and user-friendly
error communication.
"""
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def register_exception_handlers(app):
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": "Validation error", "errors": exc.errors()}
        )