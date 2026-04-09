from datetime import datetime
import requests
from laundromatic.models import HourlyForecast

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_hourly_forecast(
    latitude: float,
    longitude: float,
    days: int = 7,
):
    response = requests.get(
        OPEN_METEO_FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                #"wind_speed_10m",
            ],
            "forecast_days": days,
            "timezone": "auto",
        },
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    hourly = data["hourly"]
    forecasts = []

    for i, ts in enumerate(hourly["time"]):
        forecasts.append(
            HourlyForecast(
                timestamp=datetime.fromisoformat(ts),
                temperature_c=hourly["temperature_2m"][i],
                humidity_pct=hourly["relative_humidity_2m"][i],
                precipitation_probability=hourly["precipitation_probability"][i] / 100.0,
                #wind_speed_mps=hourly["wind_speed_10m"][i],
            )
        )

    return forecasts