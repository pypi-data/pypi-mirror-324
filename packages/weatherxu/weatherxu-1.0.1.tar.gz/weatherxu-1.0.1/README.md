# WeatherXu Python SDK

Official Python SDK for accessing WeatherXu's weather data API.

## Installation

### From PyPI
```bash
pip install weatherxu
```

### From Source
```bash
git clone https://github.com/weatherxu/weatherxu-python.git
cd weatherxu-python
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from weatherxu import WeatherXu

# Initialize the client
client = WeatherXu(api_key="YOUR_API_KEY", units="metric")

# Get current weather and forecast for New York City
weather = client.get_weather(
    lat=40.7128,
    lon=-74.0060,
    parts=['currently', 'hourly', 'daily']
)

# Print current temperature
print(f"Current temperature: {weather.currently.temperature}°C")

# Get hourly forecasts
for hour in weather.hourly:
    print(f"Time: {hour.forecast_start}, Temperature: {hour.temperature}°C")

# Get historical weather data
from datetime import datetime, timedelta

end_time = int(datetime.now().timestamp())
start_time = int((datetime.now() - timedelta(days=1)).timestamp())

historical = client.get_historical(
    lat=40.7128,
    lon=-74.0060,
    start=start_time,
    end=end_time
)

# Print historical data
for record in historical.hourly:
    print(f"Time: {record.forecast_start}, Temperature: {record.temperature}°C")
```

## Features

- Type hints and dataclasses for better IDE support
- Automatic parsing of timestamps to datetime objects
- Comprehensive error handling
- Support for both metric and imperial units
- Optional request timeout configuration

## API Reference

### Initialization

```python
WeatherXu(
    api_key: str,
    units: str = 'metric',
    timeout: int = 10
)
```

### Methods

#### get_weather()

Get current weather and forecast data for a location.

```python
get_weather(
    lat: float,
    lon: float,
    parts: Optional[List[str]] = None,
    units: Optional[str] = None
) -> WeatherData
```

Parameters:
- `lat`: Latitude (-90 to 90)
- `lon`: Longitude (-180 to 180)
- `parts`: Optional list of data blocks to include ('alerts', 'currently', 'hourly', 'daily')
- `units`: Optional unit system ('metric' or 'imperial')

#### get_historical()

Get historical weather data for a location.

```python
get_historical(
    lat: float,
    lon: float,
    start: int,
    end: int,
    units: Optional[str] = None
) -> HistoricalData
```

Parameters:
- `lat`: Latitude (-90 to 90)
- `lon`: Longitude (-180 to 180)
- `start`: Start time (Unix timestamp)
- `end`: End time (Unix timestamp)
- `units`: Optional unit system ('metric' or 'imperial')

## Error Handling

The SDK throws `WeatherError` for any API or network-related errors. Each error includes:
- Error message
- HTTP status code (when available)
- Error code (when provided by the API)

```python
try:
    weather = client.get_weather(lat=40.7128, lon=-74.0060)
except WeatherError as e:
    print(f"Error: {e}")
    if e.status_code:
        print(f"Status code: {e.status_code}")
```

## Development

### Installation

For development, you can install all development dependencies using:

```bash
pip install -r requirements-dev.txt
```

This includes:
- Testing tools (pytest, pytest-cov)
- Code formatting (black, isort)
- Type checking (mypy)
- Documentation (Sphinx)
- Code quality (flake8, pylint)

## Requirements

- Python 3.7 or higher
- requests library
