#%%
from datetime import datetime, timedelta
from laundromatic.core import HourlyForecast, find_all_drying_windows

#%%
hours = []

start_time = datetime(2026, 4, 9, 0)

for h in range(24):
    hour = HourlyForecast(
        timestamp=start_time + timedelta(hours=h),
        temperature_c=20.0,         
        humidity_pct=70.0,            
        precipitation_probability=0.0,
    )
    
    hour.no_rain = True
    hour.drying_progress = 0.25

    hours.append(hour)

hours[8].no_rain = False
hours[10].no_rain = False
hours[9].drying_progress = 0.8
hours[13].drying_progress = 0.75

find_all_drying_windows(hours)

#%%
all_windows = find_all_drying_windows(hours, required_drying=1.0, max_duration_hours=8)

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
    key=lambda w: (w["start_hour"])
)

print("Best window:", best_window)
print("Latest window:", latest_window)
# %%
