from .data_loader import SentinelHubDetaLoader
from ..utils import get_bbox
from ..show import plot_image

loader = SentinelHubDetaLoader()

info = {
    "layer": 'TRUE-COLOR-S2-L1C',
    "bbox": get_bbox(45.340833, -116.466667, r=3000),
    "time": ('2019-10-01', '2019-10-31'),
    "resx": "10m",
    "resy": "10m"
}

wcs_img = loader.load(info)
plot_image(wcs_img[-1])