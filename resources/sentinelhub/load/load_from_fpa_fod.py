from resources.fpa_fod.data_loader import FpaFodDataLoader
from .data_loader import SentinelHubDataLoader
from ..utils import get_bbox
import pandas as pd
from datetime import timedelta
import time


class SentinelLoaderFromFpaFod(object):
    def __init__(self):
        self.fpa_fod_loader = FpaFodDataLoader()
        self.sentinel_loader = SentinelHubDataLoader()

    def download(self, layer, loc=None, from_date=None, until_date=None, min_fire_size=0.0, max_cloud_coverage=0.3,
                 r=3000, resx="10m", resy="10m",
                 subdir_with_fire="with_fire", subdir_before_fire="before_fire", subdir_after_fire="after_fire"):

        one_year = timedelta(days=365)

        df = self.fpa_fod_loader.get_records(
            loc=loc, from_date=from_date, until_date=until_date, min_fire_size=min_fire_size
        ).reset_index()

        print("Found {} wildfire records...".format(len(df)))

        for i, row in df.iterrows():
            fire_lat = row["LATITUDE"]
            fire_lng = row["LONGITUDE"]
            fire_start = row["START_DATE"]
            fire_end = row["END_DATE"]

            fire_start = fire_start if fire_start is not pd.NaT else None
            fire_end = fire_end if fire_end is not pd.NaT else None

            info = {
                "layer": layer,
                "bbox": get_bbox(fire_lat, fire_lng, r=r),
                "maxcc": max_cloud_coverage,
                "resx": resx,
                "resy": resy
            }

            # download images that contain wildfire
            with_fire_array = self.sentinel_loader.load({
                **info,
                "time": (fire_start, fire_end)
            }, subdir_with_fire)

            print("With fire: {}, Start: {:%Y-%m-%d}, End: {:%Y-%m-%d}".format(len(with_fire_array), fire_start, fire_end))

            # download the same number of images taken before the wildfire
            before_fire_array = self.sentinel_loader.load({
                **info,
                "time": (fire_start - one_year, fire_end - one_year)
            }, subdir_before_fire)

            print("Before fire: {}, Start: {:%Y-%m-%d}, End: {:%Y-%m-%d}".format(len(before_fire_array), fire_start - one_year, fire_end - one_year))

            # download the same number of images taken after the wildfire
            after_fire_array = self.sentinel_loader.load({
                **info,
                "time": (fire_start + one_year, fire_end + one_year)
            }, subdir_after_fire)

            print("After fire: {}, Start: {:%Y-%m-%d}, End: {:%Y-%m-%d}".format(len(after_fire_array), fire_start + one_year, fire_end + one_year))

            if i % 10 == 0:
                print("Downloaded {}-th record".format(i))

