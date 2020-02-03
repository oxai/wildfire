from resources.modis_fire.data_loader import ModisFireDataLoader
from .data_loader import SentinelHubDataLoader
from ..utils import get_bbox_from_radius
import pandas as pd
from datetime import timedelta, datetime


class SentinelLoaderFromModis(object):
    def __init__(self):
        self.fire_loader = ModisFireDataLoader()
        self.sentinel_loader = SentinelHubDataLoader()

    def download(self, layer, bbox=None, from_date=None, until_date=None, max_cloud_coverage=0.3, r=3000, resx="10m", resy="10m", subdir="with_fire"):
        df = self.fire_loader.get_records(
            bbox=bbox, from_date=from_date, until_date=until_date
        ).reset_index()

        print("Found {} wildfire records...".format(len(df)))

        for i, row in df.iterrows():
            fire_lat = row["LATITUDE"]
            fire_lng = row["LONGITUDE"]
            date = datetime.strptime(row["DATE"], '%Y-%m-%d')
            fire_start = date - timedelta(days=4)
            fire_end = date + timedelta(days=4)

            fire_start = fire_start if fire_start is not pd.NaT else None
            fire_end = fire_end if fire_end is not pd.NaT else None

            info = {
                "layer": layer,
                "bbox": get_bbox_from_radius(fire_lat, fire_lng, r=r),
                "time": (fire_start, fire_end),
                "maxcc": max_cloud_coverage,
                "resx": resx,
                "resy": resy
            }

            imgs = self.sentinel_loader.load(info, subdir)

            print("Found %d images" % len(imgs))

            if i % 10 == 0:
                print("Downloaded {}-th record".format(i))

