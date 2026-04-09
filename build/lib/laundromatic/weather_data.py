from datetime import date
from typing import List

import requests
from laundromatic.weather_data import DailyForecast

OPEN_METEO_DAILY_URL = "https://api.open-meteo.com/v1/forecast"

def get_daily_forecast(
    latitude: float,
    longitude: float,
    days: int = 7,
) -> List[DailyForecast]:

    response = requests.get(
        OPEN_METEO_DAILY_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "relative_humidity_2m_max",
                "precipitation_probability_max",
                "wind_speed_10m_max",
            ],
            "forecast_days": days,
            "timezone": "auto",
        },
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    forecasts: List[DailyForecast] = []

    for i in range(len(data["daily"]["time"])):
        forecasts.append(
            DailyForecast(
                forecast_date=date.fromisoformat(data["daily"]["time"][i]),
                temperature_c=data["daily"]["temperature_2m_max"][i],
                humidity_pct=data["daily"]["relative_humidity_2m_max"][i],
                precipitation_probability=(
                    data["daily"]["precipitation_probability_max"][i] / 100.0
                ),
                wind_speed_mps=data["daily"]["wind_speed_10m_max"][i],
            )
        )

    return forecasts
