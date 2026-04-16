from datetime import date, datetime
import math
import numpy as np

class HourlyForecast:
    def __init__(
        self,
        timestamp,
        temperature_c,
        humidity_pct,
        precipitation_probability,
        #wind_speed_mps,
    ):        
        self.date = timestamp.date()
        self.hour = timestamp.hour
        self.temperature_c = temperature_c
        self.humidity_pct = humidity_pct
        self.precipitation_probability = precipitation_probability
        self.no_rain = None
        #self.wind_speed_mps = wind_speed_mps
        self.drying_progress = None

def arden_buck(temp_c):
    if temp_c >= 0:
        return 0.61121 * math.exp(
            (18.678 - temp_c / 234.5)
            * (temp_c / (257.14 + temp_c))
        )

def vapour_pressure_deficit(saturation_vp_kpa, humidity_pct):
    return saturation_vp_kpa * (1 - humidity_pct / 100.0)

# Baseline assumption: t_0 = 4.0 h at T_0 = 20°C, RH_0 = 70%.
temp_c_0 = 20
rh_pct_0 = 70
svp_kpa_0 = arden_buck(temp_c_0)
vpd_kpa_0 = vapour_pressure_deficit(svp_kpa_0, rh_pct_0)

def drying_progress_for_hour(temperature_c: float, humidity_pct: float):
    if temperature_c < 0:
        
        return 0.0
    
    # Estimate saturation vapour pressure in kPa using Arden Buck equation:
    else:
        saturation_vp_kpa = arden_buck(temperature_c)        
        vpd = vapour_pressure_deficit(saturation_vp_kpa, humidity_pct)
        
        return vpd / (4.0 * vpd_kpa_0) # drying progress per hour, relative to baseline

def calculate_drying_progress(hourly_forecasts, precipitation_probability_threshold):
    """
    Groups HourlyForecast objects by day and updates each in-place
    with:
      - no_rain (boolean, true if precipitation_probability <= precipitation_probability_threshold)
      - drying_progress

    Returns:
        dict[date, list[HourlyForecast]]
    """

    hourly_by_day = {}

    for hour in hourly_forecasts:
        day = hour.date

        if day not in hourly_by_day:
            hourly_by_day[day] = []

        hourly_by_day[day].append(hour)

    for hours in hourly_by_day.values():
        for hour in hours:
            hour.no_rain = hour.precipitation_probability <= precipitation_probability_threshold

            if hour.no_rain:
                hour.drying_progress = drying_progress_for_hour(
                    temperature_c=hour.temperature_c,
                    humidity_pct=hour.humidity_pct,
                )
            else:
                hour.drying_progress = 0.0

    return dict(hourly_by_day)

def find_all_drying_windows(hours, required_drying, max_duration_hours):
    """
    Finds all contiguous drying windows in a single day that
    achieve at least `required_drying`.

    Returns
    -------
    list of dict
        Each dict contains:
        {
            "start_hour": int,
            "end_hour": int,
            "duration_hours": int,
            "total_drying": float,
            "hourly_data": list[HourlyForecast],
        }
    """

    all_windows = []

    start = 0
    current_sum = 0.0

    for end in range(len(hours)):
        hour = hours[end]

        if not hour.no_rain:
            start = end + 1
            current_sum = 0.0
            continue

        current_sum += hour.drying_progress

        while current_sum >= required_drying and start <= end:
            duration = end - start + 1

            candidate = {
                "start_hour": hours[start].hour,
                "end_hour": hours[end].hour,
                "duration_hours": duration,
                "total_drying": current_sum,
                "hourly_data": hours[start:end+1],
            }

            all_windows.append(candidate)

            current_sum -= hours[start].drying_progress
            start += 1

    all_windows = [
    w for w in all_windows
    if w["duration_hours"] <= max_duration_hours
    ]
    
    return all_windows

def find_best_drying_windows(
    hourly_forecasts,
    required_drying,
    max_duration_hours,
    precipitation_threshold,
    earliest_start_hour,
    latest_end_hour,
):
    hourly_by_day = calculate_drying_progress(
        hourly_forecasts,
        precipitation_threshold
    )

    all_windows = []

    for day, hours in hourly_by_day.items():
        windows = find_all_drying_windows(
            hours,
            required_drying,
            max_duration_hours
        )

        for w in windows:
            all_windows.append({
                "date": day,
                **w,
            })

    eligible_windows = [
        w for w in all_windows
        if w["end_hour"] <= latest_end_hour - 1
        and w["start_hour"] >= earliest_start_hour
    ]

    for w in eligible_windows:
        w["end_hour"] += 1  # inclusive display

    if not eligible_windows:
        return None, None, []

    best_window = min(
        eligible_windows,
        key=lambda w: (w["duration_hours"], -w["total_drying"])
    )

    latest_window = max(
        eligible_windows,
        key=lambda w: (w["date"], w["start_hour"])
    )

    return best_window, latest_window, eligible_windows

def format_window(window):
    hourly_data = window["hourly_data"]
    
    avg_temp = sum(h.temperature_c for h in hourly_data) / len(hourly_data)
    avg_rh = sum(h.humidity_pct for h in hourly_data) / len(hourly_data)

    return (
        f"{window['date']} | "
        f"{window['start_hour']:02d}:00–{window['end_hour']:02d}:00 | "
        f"{window['duration_hours']}h | "
        f"avgT={avg_temp:.1f}°C | "
        f"avgRH={avg_rh:.0f}%"
    )
