import os, requests, zipfile

from resources.utils.gis import get_bbox_corners_for_tile, get_tile_pixel_scale_from_zoom
from .methods import get_image_download_url_for_tile, get_image_download_url
from io import BytesIO
from skimage import io
from tifffile import imsave
from skimage.transform import resize
import shutil
from .methods import TileDateRangeQuery


def save_gee_tile(base_path, ee_image, bands, q: TileDateRangeQuery, image_id, img_size):
    bbox = get_bbox_corners_for_tile(x_tile=q.x, y_tile=q.y, zoom=q.z)
    save_ee_image(base_path, ee_image, bands, image_id, bbox, q.z, img_size)


def save_ee_image(base_path, ee_image, bands: list, image_id: str, bbox: tuple or list,
                  zoom=13, img_size: int or None = None):

    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    scale = get_tile_pixel_scale_from_zoom(zoom=zoom, tile_size=img_size if img_size else 256)

    print(f"Downloading image {f'of size {img_size}x{img_size} pixels ' if img_size else ''}"
          f"with {scale:.2f} m resolution")
    url = get_image_download_url(ee_image, bbox, scale, name=image_id)
    print(url)
    r = requests.get(url)
    z = zipfile.ZipFile(BytesIO(r.content))
    z.extractall(base_path)

    imgs = [io.imread(os.path.join(base_path, f"{image_id}.{band}.tif")) for band in bands]
    out = io.concatenate_images(imgs)
    if img_size is not None:
        out = resize(out, (out.shape[0], img_size, img_size))
    imsave(f"{base_path}.tif", out)
    shutil.rmtree(base_path)

    return out
