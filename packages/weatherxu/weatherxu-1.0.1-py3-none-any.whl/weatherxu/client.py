"""
WeatherXu API client implementation.
"""

from typing import List, Optional, Union
import requests
from urllib.parse import urlencode

from .models import WeatherData, HistoricalData, WeatherError


class WeatherXu:
    """
    WeatherXu API client.

    Args:
        api_key (str): Your WeatherXu API key
        units (str, optional): Default unit system ('metric' or 'imperial'). Defaults to 'metric'.
    """

    def __init__(self, api_key: str, units: str = 'metric'):
        if not api_key:
            raise WeatherError("API key is required")

        self.api_key = api_key
        self.default_units = units
        self._weather_base_url = 'https://api.weatherxu.com/v1'
        self._historical_base_url = 'https://historical.weatherxu.com/v1'

    def get_weather(
        self,
        lat: float,
        lon: float,
        parts: Optional[List[str]] = None,
        units: Optional[str] = None
    ) -> WeatherData:
        """
        Get current weather and forecast data for a location.

        Args:
            lat (float): Latitude (-90 to 90)
            lon (float): Longitude (-180 to 180)
            parts (List[str], optional): Data blocks to include ('alerts', 'currently', 'hourly', 'daily')
            units (str, optional): Unit system ('metric' or 'imperial'). Overrides default units.

        Returns:
            WeatherData: Weather data response

        Raises:
            WeatherError: If the API request fails
        """
        params = {
            'lat': lat,
            'lon': lon,
            'units': units or self.default_units
        }

        if parts:
            params['parts'] = ','.join(parts)

        try:
            response = requests.get(
                f"{self._weather_base_url}/weather",
                params=params,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if not result.get('success', False):
                error = result.get('error', {})
                raise WeatherError(
                    error.get('message', 'Unknown error occurred'),
                    status_code=error.get('statusCode')
                )

            return WeatherData.from_dict(result)

        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if hasattr(e, 'response') else None
            if isinstance(e, requests.exceptions.HTTPError):
                message = f"Weather API request failed: {e.response.reason}"
            else:
                message = f"Failed to fetch weather data: {str(e)}"
            raise WeatherError(message, status_code=status_code)

    def get_historical(
        self,
        lat: float,
        lon: float,
        start: int,
        end: int,
        units: Optional[str] = None
    ) -> HistoricalData:
        """
        Get historical weather data for a location.

        Args:
            lat (float): Latitude (-90 to 90)
            lon (float): Longitude (-180 to 180)
            start (int): Start time (Unix timestamp)
            end (int): End time (Unix timestamp)
            units (str, optional): Unit system ('metric' or 'imperial'). Overrides default units.

        Returns:
            HistoricalData: Historical weather data response

        Raises:
            WeatherError: If the API request fails
        """
        params = {
            'lat': lat,
            'lon': lon,
            'start': start,
            'end': end,
            'units': units or self.default_units
        }

        try:
            response = requests.get(
                f"{self._historical_base_url}/history",
                params=params,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if not result.get('success', False):
                error = result.get('error', {})
                raise WeatherError(
                    error.get('message', 'Unknown error occurred'),
                    status_code=error.get('statusCode')
                )

            return HistoricalData.from_dict(result)

        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if hasattr(e, 'response') else None
            if isinstance(e, requests.exceptions.HTTPError):
                message = f"Historical API request failed: {e.response.reason}"
            else:
                message = f"Failed to fetch historical data: {str(e)}"
            raise WeatherError(message, status_code=status_code)

    def _get_headers(self) -> dict:
        """Get request headers with API key."""
        return {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }