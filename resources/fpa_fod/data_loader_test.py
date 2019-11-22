from .data_loader import FpaFodDataLoader


loader = FpaFodDataLoader()
loc = {"lat": 45, "lng": -116, "delta": 5}
df = loader.get_records(loc, from_date="2014-01-01", until_date="2015-01-01", min_fire_size=5.0)
print(df)
