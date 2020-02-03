from .load_from_modis import SentinelLoaderFromModis


loader = SentinelLoaderFromModis()
loader.download('BANDS-S2-L2A', bbox=None, from_date='2018-01-01', until_date=None, max_cloud_coverage=0.1, subdir="modis_fire")
