import ee
import urllib.request

from .methods import get_image_collection_asset

ee.Initialize()

url = get_image_collection_asset(
    platform="landsat",
    sensor="8",
    product="surface",
    date_from="2019-12-01",
    date_to="2019-12-30",
    reducer='median'
)

print(url)

with urllib.request.urlopen(url.format(z=8, x=233, y=156)) as response:
    tile = response.read()