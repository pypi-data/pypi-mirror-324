"""
Data models for the WeatherXu SDK.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

class WeatherError(Exception):
    """Custom exception for WeatherXu API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, error_code: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code


@dataclass
class Alert:
    """Weather alert information."""
    title: str
    description: str
    ends_at: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Alert':
        return cls(
            title=data['title'],
            description=data['description'],
            ends_at=data.get('endsAt')
        )


@dataclass
class CurrentConditions:
    """Current weather conditions."""
    apparent_temperature: float
    cloud_cover: float
    dew_point: float
    humidity: float
    icon: str
    precip_intensity: float
    pressure: float
    temperature: float
    uv_index: float
    visibility: float
    wind_direction: float
    wind_gust: float
    wind_speed: float

    @classmethod
    def from_dict(cls, data: dict) -> 'CurrentConditions':
        return cls(
            apparent_temperature=data['apparentTemperature'],
            cloud_cover=data['cloudCover'],
            dew_point=data['dewPoint'],
            humidity=data['humidity'],
            icon=data['icon'],
            precip_intensity=data['precipIntensity'],
            pressure=data['pressure'],
            temperature=data['temperature'],
            uv_index=data['uvIndex'],
            visibility=data['visibility'],
            wind_direction=data['windDirection'],
            wind_gust=data['windGust'],
            wind_speed=data['windSpeed']
        )


@dataclass
class HourlyCondition:
    """Hourly weather condition."""
    apparent_temperature: float
    cloud_cover: float
    dew_point: float
    forecast_start: int
    humidity: float
    icon: str
    precip_intensity: float
    precip_probability: float
    pressure: float
    temperature: float
    uv_index: float
    visibility: float
    wind_direction: float
    wind_gust: float
    wind_speed: float

    @classmethod
    def from_dict(cls, data: dict) -> 'HourlyCondition':
        return cls(
            apparent_temperature=data['apparentTemperature'],
            cloud_cover=data['cloudCover'],
            dew_point=data['dewPoint'],
            forecast_start=data['forecastStart'],
            humidity=data['humidity'],
            icon=data['icon'],
            precip_intensity=data['precipIntensity'],
            precip_probability=data['precipProbability'],
            pressure=data['pressure'],
            temperature=data['temperature'],
            uv_index=data['uvIndex'],
            visibility=data['visibility'],
            wind_direction=data['windDirection'],
            wind_gust=data['windGust'],
            wind_speed=data['windSpeed']
        )


@dataclass
class HistoricalHourlyCondition:
    """Historical hourly weather condition."""
    apparent_temperature: float
    cloud_cover: float
    dew_point: float
    forecast_start: int
    humidity: float
    icon: str
    precip_intensity: float
    pressure: float
    temperature: float
    wind_direction: float
    wind_gust: float
    wind_speed: float

    @classmethod
    def from_dict(cls, data: dict) -> 'HistoricalHourlyCondition':
        return cls(
            apparent_temperature=data['apparentTemperature'],
            cloud_cover=data['cloudCover'],
            dew_point=data['dewPoint'],
            forecast_start=data['forecastStart'],
            humidity=data['humidity'],
            icon=data['icon'],
            precip_intensity=data['precipIntensity'],
            pressure=data['pressure'],
            temperature=data['temperature'],
            wind_direction=data['windDirection'],
            wind_gust=data['windGust'],
            wind_speed=data['windSpeed']
        )


@dataclass
class DailyCondition:
    """Daily weather condition."""
    apparent_temperature_avg: float
    apparent_temperature_max: float
    apparent_temperature_min: float
    cloud_cover: float
    dew_point_avg: float
    dew_point_max: float
    dew_point_min: float
    forecast_end: int
    forecast_start: int
    humidity: float
    icon: str
    moon_phase: float
    precip_intensity: float
    precip_probability: float
    pressure: float
    sunrise_time: int
    sunset_time: int
    temperature_avg: float
    temperature_max: float
    temperature_min: float
    uv_index_max: float
    visibility: float
    wind_direction_avg: float
    wind_gust_avg: float
    wind_gust_max: float
    wind_gust_min: float
    wind_speed_avg: float
    wind_speed_max: float
    wind_speed_min: float

    @classmethod
    def from_dict(cls, data: dict) -> 'DailyCondition':
        return cls(
            apparent_temperature_avg=data['apparentTemperatureAvg'],
            apparent_temperature_max=data['apparentTemperatureMax'],
            apparent_temperature_min=data['apparentTemperatureMin'],
            cloud_cover=data['cloudCover'],
            dew_point_avg=data['dewPointAvg'],
            dew_point_max=data['dewPointMax'],
            dew_point_min=data['dewPointMin'],
            forecast_end=data['forecastEnd'],
            forecast_start=data['forecastStart'],
            humidity=data['humidity'],
            icon=data['icon'],
            moon_phase=data['moonPhase'],
            precip_intensity=data['precipIntensity'],
            precip_probability=data['precipProbability'],
            pressure=data['pressure'],
            sunrise_time=data['sunriseTime'],
            sunset_time=data['sunsetTime'],
            temperature_avg=data['temperatureAvg'],
            temperature_max=data['temperatureMax'],
            temperature_min=data['temperatureMin'],
            uv_index_max=data['uvIndexMax'],
            visibility=data['visibility'],
            wind_direction_avg=data['windDirectionAvg'],
            wind_gust_avg=data['windGustAvg'],
            wind_gust_max=data['windGustMax'],
            wind_gust_min=data['windGustMin'],
            wind_speed_avg=data['windSpeedAvg'],
            wind_speed_max=data['windSpeedMax'],
            wind_speed_min=data['windSpeedMin']
        )


@dataclass
class WeatherData:
    """Complete weather data response."""
    success: bool
    data: dict

    @classmethod
    def from_dict(cls, data: dict) -> 'WeatherData':
        return cls(
            success=data['success'],
            data={
                'dt': data['data']['dt'],
                'latitude': data['data']['latitude'],
                'longitude': data['data']['longitude'],
                'timezone': data['data']['timezone'],
                'timezone_abbreviation': data['data']['timezone_abbreviation'],
                'timezone_offset': data['data']['timezone_offset'],
                'units': data['data']['units'],
                'alerts': [Alert.from_dict(alert) for alert in data['data'].get('alerts', [])] if 'alerts' in data['data'] else None,
                'currently': CurrentConditions.from_dict(data['data']['currently']) if 'currently' in data['data'] else None,
                'hourly': {'data': [HourlyCondition.from_dict(hour) for hour in data['data']['hourly']['data']]} if 'hourly' in data['data'] else None,
                'daily': {'data': [DailyCondition.from_dict(day) for day in data['data']['daily']['data']]} if 'daily' in data['data'] else None
            }
        )


@dataclass
class HistoricalData:
    """Historical weather data response."""
    success: bool
    data: dict

    @classmethod
    def from_dict(cls, data: dict) -> 'HistoricalData':
        return cls(
            success=data['success'],
            data={
                'dt': data['data']['dt'],
                'latitude': data['data']['latitude'],
                'longitude': data['data']['longitude'],
                'timezone': data['data']['timezone'],
                'timezone_abbreviation': data['data']['timezone_abbreviation'],
                'timezone_offset': data['data']['timezone_offset'],
                'units': data['data']['units'],
                'hourly': {
                    'data': [HistoricalHourlyCondition.from_dict(hour) for hour in data['data']['hourly']['data']]
                }
            }
        )