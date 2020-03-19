import numpy as np
import math


def deg2tile(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x_tile = int((lon_deg + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x_tile, y_tile


def tile2deg(x_tile, y_tile, zoom):
    n = 2.0 ** zoom
    lon_deg = x_tile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_tile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def get_bbox_corners_for_tile(x_tile, y_tile, zoom):
    lat_upper, lng_left = tile2deg(x_tile, y_tile, zoom)
    lat_lower, lng_right = tile2deg(x_tile + 1, y_tile + 1, zoom)
    bbox = [lng_left, lat_lower, lng_right, lat_upper]
    return bbox


def get_bbox_corners_from_radius(lat_c, lng_c, r=1000):
    """Return lat and lon of lower left
       and upper right corners of bbox from center and radius.

    Parameters
    ----------
    lat_c: latitude of center point in decimal degrees.
    lng_c: longitude of center point in decimal degrees.
    r: Length of edge of square box in meters. Default 1000.

    Returns
    -------
    Y-dY: latitude of lower left corner of bounding box
    X-dX: longitude of lower left corner of bounding box
    Y+dY: latitude of upper right corner of bounding box
    X+dX: longitude of upper right corner of bounding box

    """

    X = lng_c
    Y = lat_c

    # earth circumference
    L = 40.075e6
    dY = 360 * r / L
    dX = dY / np.cos(np.radians(Y))
    return [X - dX, Y - dY, X + dX, Y + dY]


def get_tile_pixel_scale_from_zoom(zoom, tile_size=256):
    R = 6378137
    L = 2 * np.pi * R
    return L * 0.5 ** zoom / tile_size
