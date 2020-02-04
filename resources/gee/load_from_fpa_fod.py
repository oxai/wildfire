import sys
from resources.fpa_fod.data_loader import FpaFodDataLoader
from .tile_loader import GeeProductTileSeriesLoader
from datetime import timedelta
from .tile_loader_helper import download_from_df


class GEELoaderFromFpaFod(object):
    def __init__(self):
        self.fpa_fod_loader = FpaFodDataLoader()
        self.image_loader = GeeProductTileSeriesLoader()

    def download(self, ee_product, bbox, from_date, until_date, n_samples, min_fire_size=0.0, zoom=13,
                 subdir_with_fire="with_fire", subdir_no_fire="no_fire", display=True):

        df = self.fpa_fod_loader.get_records(
            bbox=bbox, from_date=from_date, until_date=until_date, min_fire_size=min_fire_size
        ).reset_index()

        print(f"Found {len(df)} wildfire records. Downloading {min(len(df), n_samples)} samples...")

        download_from_df(self.image_loader, df[:n_samples], ee_product, zoom, subdir=subdir_with_fire, display=False)

        df = self.fpa_fod_loader.get_neg_examples(
            bbox, from_date=from_date, until_date=until_date, n_samples=n_samples
        )

        print(f"Downloading {n_samples} negative samples...")

        download_from_df(self.image_loader, df, ee_product, zoom, subdir=subdir_no_fire, display=False)