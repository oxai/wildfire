import ee
import requests, zipfile, io
from .methods import get_image_download_url_for_tile, get_ee_image_from_product, get_map_tile_url, get_ee_product, get_ee_product_name
from .config import EE_CREDENTIALS


ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(
    platform="landsat",
    sensor="8",
    product="surface"
)

ee_image = get_ee_image_from_product(
    ee_product,
    date_from="2019-12-01",
    date_to="2019-12-30",
    reducer='median'
)

# url = get_map_tile_url(ee_image, vis_params)

url = get_image_download_url_for_tile(ee_image, x_tile=2, y_tile=2, zoom=3)

print(url)

# with urllib.request.urlopen(url.format(z=8, x=233, y=156)) as response:
#     tile = response.read()

r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
