"""
Module: utils.logger
--------------------

This module provides centralized logging configuration and management for the backend
application. It sets up a consistent logging format, log levels, and output handlers to
facilitate effective debugging, monitoring, and auditing of application behavior.

Key Features:
- Configurable Log Levels:
  Supports standard log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) to control
  verbosity depending on environment (development, testing, production).

- Structured Log Formatting:
  Defines a uniform log message format including timestamp, log level, module name,
  function name, and message for easy tracing and analysis.

- Multiple Output Handlers:
  Allows logs to be directed to console, files, or external log management systems.
  Supports rotating file handlers to prevent excessive log file sizes.

- Exception Logging:
  Provides utility functions to capture and log exceptions with stack traces, aiding
  in root cause diagnosis.

- Integration Ready:
  Designed to integrate seamlessly with frameworks like FastAPI, enabling middleware
  or request-level logging.

- Thread-Safe and Asynchronous Compatible:
  Ensures logging operations are safe in concurrent and async execution contexts.

Usage:
- Import the configured logger instance and use across the application for consistent
  logging.
- Use helper functions for error logging to maintain standardized error reports.
- Adjust log level via configuration or environment variables without changing code.

Benefits:
- Centralizes logging policy, making maintenance and updates straightforward.
- Improves observability and traceability of application events.
- Helps diagnose issues faster with rich, consistent log data.
- Supports compliance and auditing by preserving detailed activity records.
"""
