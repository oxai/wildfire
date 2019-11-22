from .load_from_fpa_fod import SentinelLoaderFromFpaFod


loader = SentinelLoaderFromFpaFod()
loader.download('TRUE-COLOR-S2-L1C', loc=None, from_date='2014-01-01', until_date=None, min_fire_size=10000)
