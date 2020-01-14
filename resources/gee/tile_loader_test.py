import ee
from .tile_loader import GeeTileLoader, TileQuery
from .methods import get_ee_product
from skimage import io


ee.Initialize()

loader = GeeTileLoader()

ee_product = get_ee_product(
    platform="landsat",
    sensor="8",
    product="raw"
)

query = TileQuery(x=2, y=2, z=3, date_from="2019-12-01", date_to="2019-12-30", reducer="median")

out = loader.visualise(ee_product, query)
print(out)
io.imsave("file.jpg", out)