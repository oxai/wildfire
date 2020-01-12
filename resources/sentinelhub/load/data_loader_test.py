from .data_loader import SentinelHubDataLoader
from ..utils import get_bbox_from_radius, get_bbox_for_tile
from ..show import plot_image
from sentinelhub import CRS, BBox


loader = SentinelHubDataLoader()

bbox = BBox(bbox=[-116.50500806050067, 45.31388353025577, -116.42832593949933, 45.367782469744235], crs=CRS.WGS84)
# bbox = BBox(bbox=[-116.71875, 45.089035564831015, -115.3125, 46.07323062540836], crs=CRS.WGS84)
# bbox = get_bbox_for_tile(236, 153, 8)
# bbox =  get_bbox_from_radius(45.340833, -116.466667, r=3000)

info = {
    "layer": 'TRUE-COLOR-S2-L1C',
    "bbox": bbox,
    "time": ('2019-10-15', '2019-10-31'),
    "width": 256,
    "height": 256
}

wcs_img = loader.load(info)
plot_image(wcs_img[-1])