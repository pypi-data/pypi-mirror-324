# LogInsights-Library

LogInsights-Library is a powerful library for handling the formatting of application logs and metrics to the LogInsights platform. It is designed to help you monitor, analyze, and debug your applications with ease, offering deep insights into performance, usage patterns, and system health.

## Features

- Flexible and high-performance.
- Full support for Python.
- Capture and manage logs from across your application, with support for structured and unstructured log formats.
- Define and track custom metrics to measure application performance and user interactions.
- Easily capture exceptions and errors, providing detailed context for debugging.

## Important: The Logger Must Be Configured Before Use

Before using the logger in your application, it **must be configured** with the appropriate connection details. Ensure that the logger is set up with the correct connection string, client application ID, and secret before any logging or metric capturing takes place.

## Code example

### `settings.py`

```python
from loginsights.main import LogInsightsLogger

# Configuration variables (replace with your own details)
connection_string = ""  # Replace with your connection string
client_application_id = -1  # Replace with the given client application id
secret = ""  # Replace with the given secret

config = {
    "ConnectionString": connection_string,
    "ClientApplicationId": client_application_id,
    "Secret": secret
}

# Configure the logger
LogInsightsLogger.configure(config)
```

### `app.py`

```python
from loginsights.main import LogInsightsLogger

logger = LogInsightsLogger.get_logger()

# Example of logging and metric capturing in the application
username = "testuser"  # Example username

# Log an informational message
logger.info(f"{username} has been authenticated, redirecting {username} to login")

# Add a custom metric
logger.add_metric("New Users", {"Username": username})
```
