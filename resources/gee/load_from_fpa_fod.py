import sys
from resources.fpa_fod.data_loader import FpaFodDataLoader
from .tile_loader import GeeProductTileLoader
import pandas as pd
from datetime import timedelta
from .tile_loader_helper import TileQuery
from resources.utils.gis import deg2tile
import matplotlib.pyplot as plt
import time


class GEELoaderFromFpaFod(object):
    def __init__(self):
        self.fpa_fod_loader = FpaFodDataLoader()
        self.image_loader = GeeProductTileLoader()

    def download(self, ee_product, loc=None, from_date=None, until_date=None, min_fire_size=0.0, zoom=13,
                 subdir_with_fire="with_fire", subdir_before_fire="before_fire", subdir_after_fire="after_fire",
                 display=True):

        one_year = timedelta(days=365)

        df = self.fpa_fod_loader.get_records(
            loc=loc, from_date=from_date, until_date=until_date, min_fire_size=min_fire_size
        ).reset_index()

        print(f"Found {len(df)} wildfire records...")

        for i, row in df.iterrows():
            fire_lat = row["LATITUDE"]
            fire_lng = row["LONGITUDE"]
            fire_start = row["START_DATE"]
            fire_end = row["END_DATE"]

            fire_start = fire_start if fire_start is not pd.NaT else None
            fire_end = fire_end if fire_end is not pd.NaT else None
            if fire_end:
                fire_end = fire_end + timedelta(days=1)

            x, y = deg2tile(fire_lat, fire_lng, zoom)
            query = TileQuery(x=x, y=y, z=zoom, date_from=f"{fire_start:%Y-%m-%d}", date_to=f"{fire_end:%Y-%m-%d}",
                              reducer="median")

            # download images that contain wildfire
            try:
                self.image_loader.load(ee_product, query, subdir=subdir_with_fire)
                print("Downloaded {}-th record".format(i))
            except KeyboardInterrupt:
                sys.exit()
            except:
                try:
                    time.sleep(1)  # Sometimes request works on second try
                    self.image_loader.load(ee_product, query, subdir=subdir_with_fire)
                    print(f"Downloaded {i}-th record on second try")
                except:
                    print(f"Failed to download {i}th record")
                    continue

            print(f"With fire - Start: {fire_start:%Y-%m-%d}, End: {fire_end:%Y-%m-%d}")

            if display and i % 10 == 0:
                out = self.image_loader.visualise(ee_product, query)
                print(out)
                print(f'Displaying {i}th downloaded image. To download without diplaying, pass "display=False".')
                plt.imshow(out)
                plt.show()
