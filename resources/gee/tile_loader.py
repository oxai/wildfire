from resources.base.data_loader import DataLoader
from .methods import get_ee_image_from_product, get_ee_product_name
import os
from skimage import io
from .tile_loader_helper import TileQuery, save_gee_tile
from .vis_handler import get_vis_handler


class GeeTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.img_size = img_size

    def save(self, ee_product, q: TileQuery, image_id, subdir="tmp"):
        base_path = os.path.join(self.data_subdir(subdir), image_id)
        ee_image = get_ee_image_from_product(ee_product, date_from=q.date_from, date_to=q.date_to, reducer=q.reducer)
        bands = ee_product.get('bands', [ee_product['index']])
        save_gee_tile(base_path, ee_image, bands, q, image_id, self.img_size)

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


class CustomGeeTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.img_size = img_size

    def save(self, ee_image, bands, q: TileQuery, image_id, subdir="tmp"):
        base_path = os.path.join(self.data_subdir(subdir), image_id)
        save_gee_tile(base_path, ee_image, bands, q, image_id, self.img_size)

    def load(self, product_name, query: TileQuery, subdir="tmp"):
        image_id = self.image_id(product_name, query)
        path = os.path.join(self.data_subdir(subdir), image_id + ".tif")
        img = io.imread(path)
        return img

    def image_id(self, product_name, q: TileQuery):
        return f"{product_name}__{q.date_from}_{q.date_to}_{q.reducer}_{q.z}_{q.x}_{q.y}"
