from resources.sentinelhub.fetch.data_loader import SentinelHubDetaLoader
from sentinelhub import CRS, BBox

loader = SentinelHubDetaLoader()
betsiboka_coords_wgs84 = [46.16, -16.15, 46.51, -15.58]
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)

info = {
    "layer": 'TRUE-COLOR-S2-L1C',
    "bbox": betsiboka_bbox,
    "time": '2017-12-15',
    "width": 512,
    "height": 856
}

loader.download(info)
