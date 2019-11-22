from .data_loader import FpaFodDataLoader


loader = FpaFodDataLoader()
df = loader.get_records(lat=45, lng=-116, loc_delta=5, from_date="2014-01-01", until_date="2015-01-01", min_fire_size=5.0)
print(df)