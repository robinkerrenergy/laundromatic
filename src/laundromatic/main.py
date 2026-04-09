#%%
from laundromatic.weather_data import get_daily_forecast
from laundromatic.models import calculate_drying_time_hours

forecasts = get_daily_forecast(latitude=51.51, longitude=0.13, days=10)

for forecast in forecasts:
    hours = calculate_drying_time_hours(forecast)
    print(f"{forecast.forecast_date}, T: {forecast.temperature_c}, RH: {forecast.humidity_pct}, Drying Time: {hours}")
# %%
#TODO: create functionality for CLI (not sure if in here or another file)
