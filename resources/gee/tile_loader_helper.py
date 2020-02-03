import os, requests, zipfile

from .tile_loader import GeeProductTileSeriesLoader
from .methods import get_image_download_url_for_tile
from io import BytesIO
from skimage import io
from tifffile import imsave
from skimage.transform import resize
import shutil
from .methods import TileDateRangeQuery
from resources.utils.gis import deg2tile
import matplotlib.pyplot as plt
import sys


def save_gee_tile(base_path, ee_image, bands, q: TileDateRangeQuery, image_id, img_size):
    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    url = get_image_download_url_for_tile(ee_image, x_tile=q.x, y_tile=q.y, zoom=q.z, name=image_id)
    print(url)
    r = requests.get(url)
    z = zipfile.ZipFile(BytesIO(r.content))
    z.extractall(base_path)

    imgs = [io.imread(os.path.join(base_path, f"{image_id}.{band}.tif")) for band in bands]
    out = io.concatenate_images(imgs)
    out = resize(out, (out.shape[0], img_size, img_size))
    imsave(f"{base_path}.tif", out)
    shutil.rmtree(base_path)


def download_from_df(df, ee_product, zoom, subdir, display=False):
    image_loader = GeeProductTileSeriesLoader()
    for i, record in df.iterrows():
        lat = record["LATITUDE"]
        lng = record["LONGITUDE"]
        start_date = record["START_DATE"]
        end_date = record["END_DATE"]

        start_date = f"{start_date:%Y-%m-%d}" if start_date is not pd.NaT else None
        end_date = f"{end_date:%Y-%m-%d}" if end_date is not pd.NaT else None

        x, y = deg2tile(lat, lng, zoom)
        query = TileDateRangeQuery(x=x, y=y, z=zoom, date_from=start_date, date_to=end_date,
                                   reducer="median")

        print(f"Downloading {i}th record. (x, y) = ({x}, {y}), {start_date} to s{end_date}")

        # download images that contain wildfire
        try:
            image_loader.load(ee_product, query, subdir=subdir)
        except KeyboardInterrupt:
            sys.exit()

        print(f"Downloaded {i}th record. (x, y) = ({x}, {y}), {start_date} to s{end_date}")

        if display and i % 10 == 0:
            out = image_loader.visualise(ee_product, query)
            print(out)
            print(f'Displaying {i}th downloaded image. To download without diplaying, pass "display=False".')
            plt.imshow(out)
            plt.show()
