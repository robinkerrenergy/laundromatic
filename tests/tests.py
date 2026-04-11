#%%
from laundromatic.core import drying_progress_for_hour

for T in [-5, 5, 10, 15, 20]:
    progress = drying_progress_for_hour(T, humidity_pct=60)
    print(T, progress)
# %%
for RH in [40, 60, 80, 95, 100]:
    progress = drying_progress_for_hour(20, RH)
    print(RH, progress)
# %%

progress = drying_progress_for_hour(20, 70)
print(progress)

# %%
from datetime import datetime, timedelta
from laundromatic.models import HourlyForecast, find_all_drying_windows

hours = []

start_time = datetime(2026, 4, 9, 0)

for h in range(24):
    hour = HourlyForecast(
        timestamp=start_time + timedelta(hours=h),
        temperature_c=20.0,          # arbitrary
        humidity_pct=70.0,            # arbitrary
        precipitation_probability=0.0,
    )
    
    hour.no_rain = True
    hour.drying_progress = 0.25

    hours.append(hour)

print(hours)

hours[8].no_rain = False
hours[10].no_rain = False
hours[9].drying_progress = 0.8
hours[13].drying_progress = 0.75
print(hours[13].drying_progress)

# %%
find_all_drying_windows(hours)
# %%
all_windows = find_all_drying_windows(hours)

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
# %%
print("Best window:", best_window)
print("Latest window:", latest_window)
# %%
