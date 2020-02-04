import ee
from .config import EE_CREDENTIALS

from .load_from_fpa_fod import GEELoaderFromFpaFod
from .methods import get_ee_product


ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(
    platform="landsat",
    sensor="8",
    product="surface"
)

loader = GEELoaderFromFpaFod()
bbox = [-120, 30, -85, 45]
loader.download(ee_product, bbox=bbox, from_date='2015-08-01', until_date='2015-12-31',
                n_samples=1000, min_fire_size=10000, display=False, subdir_with_fire="fire_landsat")
