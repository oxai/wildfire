from resources.fpa_fod.data_loader import FpaFodDataLoader
import ee

from resources.gee.load_from_fpa_fod_helper import download_from_df, get_arguments
from .config import EE_CREDENTIALS


class GEELoaderFromFpaFod(object):
    def __init__(self):
        self.fpa_fod_loader = FpaFodDataLoader()

    def download(self, ee_product, bbox, from_date, until_date, n_samples, subdir, pos_examples=True,
                 min_fire_size=0.0, zoom=13, display=True):

        if pos_examples:
            df = self.fpa_fod_loader.get_records(
                bbox=bbox, from_date=from_date, until_date=until_date, min_fire_size=min_fire_size
            ).reset_index()

            print(f"Found {len(df)} wildfire records. Downloading {min(len(df), n_samples)} records...")

            download_from_df(df[:n_samples], ee_product, zoom, subdir=subdir, display=display)

        else:
            df = self.fpa_fod_loader.get_neg_examples(
                bbox, from_date=from_date, until_date=until_date, n_samples=n_samples
            )

            print(f"Downloading {n_samples} negative samples...")

            download_from_df(df, ee_product, zoom, subdir=subdir, display=display)


if __name__ == "__main__":
    ee.Initialize(EE_CREDENTIALS)

    args, ee_product, subdir = get_arguments()

    loader = GEELoaderFromFpaFod()
    loader.download(ee_product, bbox=args.bbox, from_date=args.from_date, until_date=args.until_date,
                    n_samples=args.n_samples, subdir=subdir, min_fire_size=args.min_fire_size, display=False)
