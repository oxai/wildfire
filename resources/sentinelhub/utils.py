from sentinelhub import CRS, BBox
from resources.utils.gis import get_bbox_corners_from_radius, get_bbox_corners_for_tile


def get_bbox_from_radius(lat_c, lng_c, r=1000):
    bbox = get_bbox_corners_from_radius(lat_c, lng_c, r)
    # print(bbox)
    return BBox(bbox=bbox, crs=CRS.WGS84)


def get_bbox_for_tile(x_tile, y_tile, zoom):
    bbox = get_bbox_corners_for_tile(x_tile, y_tile, zoom)
    # print(bbox)
    return BBox(bbox=bbox, crs=CRS.WGS84)
