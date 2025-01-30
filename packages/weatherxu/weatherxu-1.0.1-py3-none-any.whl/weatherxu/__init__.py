"""
WeatherXu Official Python SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python SDK for accessing WeatherXu's weather data API.

Basic usage:

    >>> from weatherxu import WeatherXu
    >>> client = WeatherXu(api_key="YOUR_API_KEY")
    >>> weather = client.get_weather(lat=40.7128, lon=-74.0060)
    >>> print(weather.currently.temperature)

:copyright: (c) 2025 WeatherXu
:license: MIT
"""

__title__ = "weatherxu"
__version__ = "1.0.0"
__author__ = "WeatherXu"
__license__ = "MIT"
__copyright__ = "Copyright 2025 WeatherXu"

from .client import WeatherXu
from .models import WeatherData, HistoricalData, WeatherError

__all__ = ["WeatherXu", "WeatherData", "HistoricalData", "WeatherError"]