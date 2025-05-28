"""
Module: db.crud
----------------

This module contains the collection of CRUD (Create, Read, Update, Delete) operations
implemented for each database table/model used in the application. It serves as the
data access layer, abstracting direct interaction with the database and encapsulating
business logic related to data manipulation.

Key Responsibilities:
- Define reusable and composable functions for creating, retrieving, updating,
  and deleting records for each table/model (e.g., User, Location, WeatherHistory).
- Implement input validation and enforce database constraints
  to maintain data integrity.
- Handle and propagate database-related exceptions such as unique constraint violations,
  foreign key errors, and connection failures with appropriate error handling.
- Support filtering, pagination, and sorting options for read operations to
  efficiently query large datasets.
- Ensure atomicity and consistency using transactions for multi-step operations
  when needed.
- Provide clear return types and error signaling for use in service and API layers.
- Facilitate unit testing by isolating database interaction logic from business logic.
- Log significant CRUD actions and errors for audit and debugging purposes.

Error Handling:
- Catch and handle common database exceptions (e.g., IntegrityError, OperationalError).
- Raise application-specific exceptions or return error codes/messages as appropriate.
- Ensure that sessions are properly managed and closed to prevent resource leaks.

Typical Usage:
- Called by service layer or API endpoints to perform database operations.
- Used with dependency-injected database sessions to maintain request scope.
- Integrate seamlessly with Pydantic schemas for input/output validation.

Integration Points:
- SQLAlchemy ORM session and models.
- Database transaction management.
- Application-level error handling middleware.

This module is critical for robust, maintainable, and secure data access, ensuring
that all interactions with the persistence layer are consistent and error-resilient.
"""
