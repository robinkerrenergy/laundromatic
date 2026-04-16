#%%
from laundromatic.weather_data import get_hourly_forecast
from laundromatic.core import find_best_drying_windows, format_window
from laundromatic.locations import get_location
from laundromatic.cli import parse_args

args = parse_args()
print("Loading forecast data...")
if args.location:
    loc = get_location(args.location)
    lat, lon = loc.lat, loc.lon
    print(f"Forecast loaded for location '{args.location}' ({lat}, {lon}). Processing data...")
else:
    lat, lon = args.lat, args.lon
    print(f"Forecast loaded for location ({lat}, {lon}). Processing data...")

hourly_forecasts = get_hourly_forecast(latitude=lat, longitude=lon, days=args.days)

best_window, latest_window, eligible_windows = find_best_drying_windows(
    hourly_forecasts,
    args.required_drying,
    args.max_duration_hours,
    args.precipitation_probability_threshold,
    args.earliest_start_hour,
    args.latest_end_hour,
)

print("\n----------------------------\nLaundromatic drying forecast\n----------------------------\n")

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
