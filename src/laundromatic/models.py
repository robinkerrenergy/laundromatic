from dataclasses import dataclass
from datetime import date
import math

class DailyForecast:
    def __init__(
        self,
        forecast_date,
        temperature_c,
        humidity_pct,
        precipitation_probability,
        wind_speed_mps,
    ):
        self.forecast_date = forecast_date
        self.temperature_c = temperature_c
        self.humidity_pct = humidity_pct
        self.precipitation_probability = precipitation_probability
        self.wind_speed_mps = wind_speed_mps
        self.drying_time_hours = None 

def calculate_drying_time_hours(forecast):
    saturation_vp = 0.61121 * math.exp(
        (18.678 - forecast.temperature_c / 234.5)
        * (forecast.temperature_c / (257.14 + forecast.temperature_c))
    )

    vpd = saturation_vp * (1 - forecast.humidity_pct / 100.0)

    if vpd <= 0:
        return float("inf")

    drying_time = 2.0 * 0.70 / vpd
    print(f"date: {forecast.forecast_date}")
    print(f"temperature_c: {forecast.temperature_c} °C")
    print(f"humidity_pct: {forecast.humidity_pct} %")
    print(f"saturation_vp: {saturation_vp:.2f} kPa")
    print(f"VPD: {vpd:.2f} kPa")
    print(f"Drying Time: {drying_time:.2f} hours")
    return max(drying_time, 1.0)

#TODO: calculate baseline VPD (don't hardcode) just once, to avoid hardcoding 0.7
#TODO: define baseline drying time (don't hardcode) just once, to avoid hardcoding 2.0
#TODO: define Arden Buck constants at the top, then use variables (again, to avoid hardcoding)