from .data_loader import FpaFodDataLoader


loader = FpaFodDataLoader()
bbox = [-120, 40, -110, 50]
df = loader.get_records_in_range(bbox, from_date="2014-01-01", until_date="2015-01-01", min_fire_size=5.0)
print(df)
