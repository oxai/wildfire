import os, requests, zipfile
from .methods import get_image_download_url_for_tile
from collections import namedtuple
from io import BytesIO
from skimage import io
from skimage.transform import resize
import shutil


TileQuery = namedtuple("Query", "x y z date_from date_to reducer")


def save_gee_tile(base_path, ee_image, bands, q: TileQuery, image_id, img_size):
    if not os.path.exists(base_path):
        url = get_image_download_url_for_tile(ee_image, x_tile=q.x, y_tile=q.y, zoom=q.z, name=image_id)
        print(url)
        r = requests.get(url)
        z = zipfile.ZipFile(BytesIO(r.content))
        z.extractall(base_path)

    imgs = [io.imread(os.path.join(base_path, f"{image_id}.{band}.tif")) for band in bands]
    out = io.concatenate_images(imgs)
    out = resize(out, (out.shape[0], img_size, img_size))
    io.imsave(f"{base_path}.tif", out)
    shutil.rmtree(base_path)