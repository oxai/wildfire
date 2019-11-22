from resources.fpa_fod.data_loader import FpaFodDataLoader
from .data_loader import SentinelHubDataLoader
from ..utils import get_bbox
import pandas as pd


class SentinelLoaderFromFpaFod(object):
    def __init__(self, subdir="with_fire"):
        self.fpa_fod_loader = FpaFodDataLoader()
        self.sentinel_loader = SentinelHubDataLoader(subdir=subdir)

    def download(self, layer, loc=None, from_date=None, until_date=None, min_fire_size=0.0, max_cloud_coverage=0.3, r=3000, resx="10m", resy="10m"):
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
                "time": (fire_start, fire_end),
                "maxcc": max_cloud_coverage,
                "resx": resx,
                "resy": resy
            }

            self.sentinel_loader.download(info)

            if i % 10 == 0:
                print("Downloaded {}-th record".format(i))

