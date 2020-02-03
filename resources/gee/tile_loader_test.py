import ee
from .tile_loader import GeeProductTileLoader, TileDateRangeQuery
from .methods import get_ee_product
from .config import EE_CREDENTIALS
import matplotlib.pyplot as plt


ee.Initialize(EE_CREDENTIALS)

loader = GeeProductTileLoader()

ee_product = get_ee_product(
    platform="modis",
    sensor="terra",
    product="temperature"
)

query = TileDateRangeQuery(x=2, y=3, z=3, date_from="2019-12-01", date_to="2019-12-30", reducer="median")

out = loader.visualise(ee_product, query)
print(out)
plt.imshow(out)
plt.show()