import sys
from resources.fpa_fod.data_loader import FpaFodDataLoader
from .tile_loader import GeeProductTileSeriesLoader
from datetime import timedelta
from .tile_loader_helper import download_from_df


class GEELoaderFromFpaFod(object):
    def __init__(self):
        self.fpa_fod_loader = FpaFodDataLoader()

    def download(self, ee_product, bbox=None, from_date=None, until_date=None, min_fire_size=0.0, zoom=13,
                 subdir_with_fire="with_fire", subdir_before_fire="before_fire", subdir_after_fire="after_fire",
                 display=True):

        df = self.fpa_fod_loader.get_records(
            bbox=bbox, from_date=from_date, until_date=until_date, min_fire_size=min_fire_size
        ).reset_index()

        print(f"Found {len(df)} wildfire records...")

        download_from_df(df, ee_product, zoom, subdir=subdir_with_fire, display=False)