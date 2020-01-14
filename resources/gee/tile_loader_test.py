import ee
from .tile_loader import GeeTileLoader, Query
from .methods import get_ee_product


ee.Initialize()

loader = GeeTileLoader()

ee_product = get_ee_product(
    platform="landsat",
    sensor="8",
    product="raw"
)

query = Query(x=2, y=2, z=3, date_from="2019-12-01", date_to="2019-12-30", reducer="median")

loader.load(ee_product, query)
