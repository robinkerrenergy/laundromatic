#%%
import pandas as pd
from importlib.resources import files

class Location:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

_LOCATIONS = {}

csv_path = files("laundromatic.data") / "nuts1_uk.csv"
nuts1_locs = pd.read_csv(csv_path)
nuts1_locs = (
    nuts1_locs.rename(columns={"NUTS118NM": "location", "LONG": "long", "LAT": "lat"})
    [["location", "lat", "long"]]
)

for _, row in nuts1_locs.iterrows():
    _LOCATIONS[row["location"]] = Location(
        name=row["location"],
        lat=row["lat"],
        lon=row["long"]
    )

def get_location(name):
    if name not in _LOCATIONS:
        raise ValueError(f"Unknown location '{name}'. Supported: {list(_LOCATIONS.keys())}")

    return _LOCATIONS[name]
