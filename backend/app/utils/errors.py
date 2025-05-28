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
from pydantic import ValidationError as PydanticValidationError


import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_408_REQUEST_TIMEOUT,
)

logger = logging.getLogger(__name__)

# --- Custom Exception Classes ---

class CustomValidationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class NotFoundError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class DuplicateEntryError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class ExternalAPIError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class DatabaseError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class AuthorizationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class ConflictError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class SerializationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class TimeoutError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


# --- Global Exception Handlers ---
async def validation_error_handler(request: Request, exc: PydanticValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "Validation error", "errors": exc.errors()},
    )

async def validation_exception_handler(request: Request, exc: CustomValidationError):
    logger.error(f"Validation error: {exc.detail}")
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"error": exc.detail})

async def not_found_exception_handler(request: Request, exc: NotFoundError):
    logger.error(f"Not found error: {exc.detail}")
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"error": exc.detail})

async def duplicate_entry_exception_handler(request: Request, exc: DuplicateEntryError):
    logger.error(f"Duplicate entry error: {exc.detail}")
    return JSONResponse(status_code=HTTP_409_CONFLICT, content={"error": exc.detail})

async def external_api_exception_handler(request: Request, exc: ExternalAPIError):
    logger.error(f"External API error: {exc.detail}")
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": exc.detail})

async def database_exception_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {exc.detail}")
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": exc.detail})

async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    logger.error(f"Authorization error: {exc.detail}")
    return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"error": exc.detail})

async def conflict_exception_handler(request: Request, exc: ConflictError):
    logger.error(f"Conflict error: {exc.detail}")
    return JSONResponse(status_code=HTTP_409_CONFLICT, content={"error": exc.detail})

async def serialization_exception_handler(request: Request, exc: SerializationError):
    logger.error(f"Serialization error: {exc.detail}")
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": exc.detail})

async def timeout_exception_handler(request: Request, exc: TimeoutError):
    logger.error(f"Timeout error: {exc.detail}")
    return JSONResponse(status_code=HTTP_408_REQUEST_TIMEOUT, content={"error": exc.detail})

# Optional: handle FastAPI/Pydantic validation errors uniformly
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": "Invalid request", "details": exc.errors()},
    )

def register_exception_handlers(app):
    app.add_exception_handler(PydanticValidationError, validation_error_handler)
    app.add_exception_handler(CustomValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(DuplicateEntryError, duplicate_entry_exception_handler)
    app.add_exception_handler(ExternalAPIError, external_api_exception_handler)
    app.add_exception_handler(DatabaseError, database_exception_handler)
    app.add_exception_handler(AuthorizationError, authorization_exception_handler)
    app.add_exception_handler(ConflictError, conflict_exception_handler)
    app.add_exception_handler(SerializationError, serialization_exception_handler)
    app.add_exception_handler(TimeoutError, timeout_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


# --- Registration 예시 (main.py에서) ---
#
# from fastapi import FastAPI
# from utils.errors import (
#     validation_exception_handler,
#     not_found_exception_handler,
#     ...
#     request_validation_exception_handler,
# )
# 
# app = FastAPI()
# 
# app.add_exception_handler(CustomValidationError, validation_exception_handler)
# app.add_exception_handler(NotFoundError, not_found_exception_handler)
# app.add_exception_handler(DuplicateEntryError, duplicate_entry_exception_handler)
# app.add_exception_handler(ExternalAPIError, external_api_exception_handler)
# app.add_exception_handler(DatabaseError, database_exception_handler)
# app.add_exception_handler(AuthorizationError, authorization_exception_handler)
# app.add_exception_handler(ConflictError, conflict_exception_handler)
# app.add_exception_handler(SerializationError, serialization_exception_handler)
# app.add_exception_handler(TimeoutError, timeout_exception_handler)
# app.add_exception_handler(RequestValidationError, request_validation_exception_handler)