from .indices import get_nbr
from ..load.data_loader import SentinelHubDataLoader
from ..utils import get_bbox
from ..show import plot_image

loader = SentinelHubDataLoader()

info = {
    "layer": 'BANDS-S2-L2A',
    "bbox": get_bbox(45.340833, -116.466667, r=3000),
    "time": ('2019-10-01', '2019-10-31'),
    "resx": "10m",
    "resy": "10m"
}

wcs_img = loader.load(info)

image = get_nbr(wcs_img[-1])
plot_image(image)
