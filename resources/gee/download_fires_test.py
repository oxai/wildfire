import ee

from resources.fpa_fod.data_loader import FpaFodDataLoader
from resources.gee.download_fires import download_fire_images
from .config import EE_CREDENTIALS
from .methods import get_ee_product


ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(
    platform="landsat",
    sensor="8",
    product="surface"
)

bbox = [-120, 30, -85, 45]
fire_loader = FpaFodDataLoader()

download_fire_images(fire_loader, ee_product, bbox=bbox, from_date='2015-08-01', until_date='2015-12-31',
                     n_samples=1000, subdir="tmp", pos_examples=True,
                     zoom=13, img_size=16, min_fire_size=0.1, display=True)
