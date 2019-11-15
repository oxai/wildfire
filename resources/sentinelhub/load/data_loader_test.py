from resources.sentinelhub.load.data_loader import SentinelHubDetaLoader
from sentinelhub import CRS, BBox

loader = SentinelHubDetaLoader()
betsiboka_coords_wgs84 = [46.16, -16.15, 46.51, -15.58]
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)

info = {
    "layer": 'TRUE-COLOR-S2-L1C',
    "bbox": betsiboka_bbox,
    "time": ('2017-12-01','2017-12-31'),
    "resx": "10m",
    "resy": "10m"
}

loader.load(info)
