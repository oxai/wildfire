from .load_from_modis import SentinelLoaderFromModis


loader = SentinelLoaderFromModis()
loader.download('TRUE-COLOR-S2-L1C', loc=None, from_date='2018-01-01', until_date=None)
