#%%
from laundromatic.weather_data import get_hourly_forecast
from laundromatic.models import calculate_drying_progress, find_all_drying_windows

hourly_forecasts = get_hourly_forecast(latitude=51.51, longitude=0.13, days=7)
hourly_by_day = calculate_drying_progress(hourly_forecasts)

daily_candidates = {}
for day, hours in hourly_by_day.items():
    daily_candidates[day] = find_all_drying_windows(hours)

all_windows = []

for day, windows in daily_candidates.items():
    for w in windows:
        all_windows.append(
            {
                "date": day,
                **w,
            }
        )

latest_end_hour = 20
eligible_windows = [
    w for w in all_windows
    if w["end_hour"] <= latest_end_hour - 1
]

best_window = min(
    eligible_windows,
    key=lambda w: (w["duration_hours"], -w["total_drying"])
)

latest_window = max(
    eligible_windows,
    key=lambda w: (w["date"], w["start_hour"])
)


# %%
#TODO: set NUTS1 locations by coordinates, and allow user to select location by name (e.g. "London") instead of lat/lon
#TODO: create functionality for CLI (not sure if in here or another file)
#TODO: make latest_end_hour user-configurable (with 20 as the default).
#TODO: make CLI somewhat usable without README. Upon startup, it should provide basic use instructions. 