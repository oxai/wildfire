from resources.base.data_loader import DataLoader
from .methods import get_ee_image_from_product, get_ee_product_name, get_image_download_url_for_tile, visualise_image
import os, requests, zipfile
from io import BytesIO
from skimage import io
from skimage.transform import resize
from collections import namedtuple
import shutil


TileQuery = namedtuple("Query", "x y z date_from date_to reducer")


class GeeTileLoader(DataLoader):
    def __init__(self):
        super().__init__()
        self.img_size = 256

    def save(self, ee_product, q: TileQuery, image_id):
        base_path = os.path.join(self.data_dir(), image_id)
        if not os.path.exists(base_path):
            ee_image = get_ee_image_from_product(ee_product, date_from=q.date_from, date_to=q.date_to, reducer=q.reducer)
            url = get_image_download_url_for_tile(ee_image, x_tile=q.x, y_tile=q.y, zoom=q.z, name=image_id)

            r = requests.get(url)
            z = zipfile.ZipFile(BytesIO(r.content))
            z.extractall(base_path)

        imgs = []
        for band in ee_product['bands']:
            sub_path = os.path.join(base_path, f"{image_id}.{band}.tif")
            img = io.imread(sub_path)
            imgs.append(img)
        out = io.concatenate_images(imgs)
        out = resize(out, (out.shape[0], self.img_size, self.img_size))
        io.imsave(f"{base_path}.tif", out)
        shutil.rmtree(base_path)

    def load(self, ee_product, query: TileQuery):
        image_id = self.image_id(ee_product, query)
        path = os.path.join(self.data_dir(), image_id + ".tif")
        if not os.path.exists(path):
            self.save(ee_product, query, image_id)

        img = io.imread(path)
        return img

    def image_id(self, ee_product, q: TileQuery):
        product_name = get_ee_product_name(ee_product)
        return f"{product_name}__{q.date_from}_{q.date_to}_{q.reducer}_{q.z}_{q.x}_{q.y}"

    def visualise(self, ee_product, query: TileQuery, vis_params=None):
        image = self.load(ee_product, query)
        out = visualise_image(ee_product, image, vis_params)
        return out.transpose(1, 2, 0)
