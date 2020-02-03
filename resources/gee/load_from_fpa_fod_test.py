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
loader.download(ee_product, bbox=None, from_date='2015-08-01', until_date=None, min_fire_size=10000, display=False,
                subdir_with_fire="fire_landsat")
