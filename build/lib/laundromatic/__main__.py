#%%
from laundromatic.weather_data import get_hourly_forecast
from laundromatic.core import calculate_drying_progress, find_all_drying_windows, format_window
from laundromatic.locations import get_location
from laundromatic.cli import parse_args

print("Loading forecast data...")
args = parse_args()
if args.location:
    loc = get_location(args.location)
    lat, lon = loc.lat, loc.lon
    print(f"Forecast loaded for location '{args.location}' ({lat}, {lon}). Processing data...")
else:
    lat, lon = args.lat, args.lon
    print(f"Forecast loaded for location ({lat}, {lon}). Processing data...")

hourly_forecasts = get_hourly_forecast(latitude=lat, longitude=lon, days=args.days)
hourly_by_day = calculate_drying_progress(hourly_forecasts, args.precipitation_probability_threshold)

daily_candidates = {}
for day, hours in hourly_by_day.items():
    daily_candidates[day] = find_all_drying_windows(hours, args.required_drying, args.max_duration_hours)

all_windows = []

for day, windows in daily_candidates.items():
    for w in windows:
        all_windows.append(
            {
                "date": day,
                **w,
            }
        )

latest_end_hour = args.latest_end_hour
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

print("\nLaundromatic drying forecast\n")

if not eligible_windows:
    print("No suitable drying windows found.")
else:
    print("Best window:")
    print("   ", format_window(best_window))

    print("\nLatest possible window:")
    print("   ", format_window(latest_window))

    if args.show_all:
        print("\nAll eligible windows:")
        for w in sorted(eligible_windows, key=lambda w: (w["date"], w["start_hour"])):
            print("   ", format_window(w))

# %%
#TODO: set NUTS1 locations by coordinates, and allow user to select location by name (e.g. "London") instead of lat/lon
#TODO: create functionality for CLI (not sure if in here or another file)
#TODO: make latest_end_hour user-configurable (with 20 as the default).
#TODO: make CLI somewhat usable without README. Upon startup, it should provide basic use instructions. 
