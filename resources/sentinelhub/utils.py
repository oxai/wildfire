import numpy as np
from sentinelhub import CRS, BBox


def get_bbox(lat_c, lng_c, r=1000):
    return BBox(bbox=get_bbox_corners(lat_c, lng_c, r), crs=CRS.WGS84)


def get_bbox_corners(lat_c, lng_c, r=1000):
    """Return lat and lon of lower left
       and upper right corners of bbox from center and radius.

    Parameters
    ----------
    lat_c: latitude of center point in decimal degrees.
    lng_c: longitude of center point in decimal degrees.
    r: Length of edge of square box in meters. Default 1000.

    Returns
    -------
    Y-dY: latitude of upper left corner of bounding box
    X-dX: longitude of upper left corner of bounding box
    Y+dY: latitude of lower right corner of bounding box
    X+dX: longitude of lower right corner of bounding box

    """

    X = lng_c
    Y = lat_c

    # earth circumference
    L = 40.075e6
    dY = 360 * r / L
    dX = dY / np.cos(np.radians(Y))
    return [X - dX, Y - dY, X + dX, Y + dY]