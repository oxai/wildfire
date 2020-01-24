from resources.base.data_loader import DataLoader
from .methods import get_ee_image_from_product, get_ee_product_name, get_image_download_url_for_tile
import os, requests, zipfile
from io import BytesIO
from skimage import io
from skimage.transform import resize
from collections import namedtuple
import shutil
from .vis_handler import get_vis_handler


TileQuery = namedtuple("Query", "x y z date_from date_to reducer")


class GeeTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.img_size = img_size

    def save(self, ee_product, q: TileQuery, image_id, subdir="tmp"):
        base_path = os.path.join(self.data_subdir(subdir), image_id)
        if not os.path.exists(base_path):
            ee_image = get_ee_image_from_product(ee_product, date_from=q.date_from, date_to=q.date_to, reducer=q.reducer)
            url = get_image_download_url_for_tile(ee_image, x_tile=q.x, y_tile=q.y, zoom=q.z, name=image_id)
            print(url)
            r = requests.get(url)
            z = zipfile.ZipFile(BytesIO(r.content))
            z.extractall(base_path)

        bands = ee_product.get('bands', [ee_product['index']])
        imgs = [io.imread(os.path.join(base_path, f"{image_id}.{band}.tif")) for band in bands]
        out = io.concatenate_images(imgs)
        out = resize(out, (out.shape[0], self.img_size, self.img_size))
        io.imsave(f"{base_path}.tif", out)
        shutil.rmtree(base_path)

    def load(self, ee_product, query: TileQuery, subdir="tmp"):
        image_id = self.image_id(ee_product, query)
        path = os.path.join(self.data_subdir(subdir), image_id + ".tif")
        if not os.path.exists(path):
            self.save(ee_product, query, image_id)

        img = io.imread(path)
        return img

    def image_id(self, ee_product, q: TileQuery):
        product_name = get_ee_product_name(ee_product)
        return f"{product_name}__{q.date_from}_{q.date_to}_{q.reducer}_{q.z}_{q.x}_{q.y}"

    def visualise(self, ee_product, query: TileQuery, handler=None, vis_params=None, method='default'):
        image = self.load(ee_product, query)
        if not handler:
            handler = get_vis_handler(ee_product, method=method)
        if not vis_params:
            vis_params = ee_product.get('vis_params', {})
        out = handler(ee_product, image, vis_params)
        return out
