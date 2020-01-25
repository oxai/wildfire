from resources.base.data_loader import DataLoader
from .methods import get_ee_image_from_product, get_ee_product_name, get_ee_collection_from_product, get_ee_image_list_from_collection
import os
from tifffile import imread
from .tile_loader_helper import TileQuery, save_gee_tile
from .vis_handler import get_vis_handler


class GeeImageTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.img_size = img_size

    def save(self, image_id, ee_image, bands, q: TileQuery, subdir="tmp"):
        base_path = os.path.join(self.data_subdir(subdir), image_id)
        if not os.path.exists(base_path+".tif"):
            save_gee_tile(base_path, ee_image, bands, q, image_id, self.img_size)
        return base_path+".tif"

    def load(self, image_id, query: TileQuery, subdir="tmp"):
        path = os.path.join(self.data_subdir(subdir), image_id + ".tif")
        img = imread(path)
        return img


class GeeProductTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.image_loader = GeeImageTileLoader(img_size=img_size)

    def save(self, ee_product, q: TileQuery, subdir="tmp"):
        image_id = self.image_id(ee_product, q)
        ee_image = get_ee_image_from_product(ee_product, date_from=q.date_from, date_to=q.date_to, reducer=q.reducer)
        bands = ee_product.get('bands', [ee_product['index']])
        return self.image_loader.save(image_id, ee_image, bands, q, subdir=subdir)

    def load(self, ee_product, query: TileQuery, subdir="tmp"):
        path = self.save(ee_product, query, subdir=subdir)
        return imread(path)

    def image_id(self, ee_product, q: TileQuery):
        product_name = get_ee_product_name(ee_product)
        return f"{product_name}__{q.date_from}_{q.date_to}_{q.reducer}_{q.z}_{q.x}_{q.y}"

    def visualise(self, ee_product, query: TileQuery, handler=None, vis_params=None, method='default', subdir="tmp"):
        image = self.load(ee_product, query, subdir=subdir)
        if not handler:
            handler = get_vis_handler(ee_product, method=method)
        if not vis_params:
            vis_params = ee_product.get('vis_params', {})
        out = handler(ee_product, image, vis_params)
        return out


class GeeProductTileSeriesLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.image_loader = GeeImageTileLoader(img_size=img_size)

    def save(self, ee_product, q: TileQuery, subdir="tmp"):
        bands = ee_product.get('bands', [ee_product['index']])
        ee_collection = get_ee_collection_from_product(ee_product, date_from=q.date_from, date_to=q.date_to)
        ee_images = get_ee_image_list_from_collection(ee_collection)
        paths = []
        for ee_image in ee_images:
            image_id = self.image_id(ee_product, ee_image.get("system:index").getInfo().replace("_", "-"), q)
            path = self.image_loader.save(image_id, ee_image, bands, q, subdir=subdir)
            paths.append(path)
        return paths

    def load(self, ee_product, q: TileQuery, subdir="tmp"):
        paths = self.save(ee_product, q, subdir=subdir)
        return [imread(path) for path in paths]

    def image_id(self, ee_product, date, q: TileQuery):
        product_name = get_ee_product_name(ee_product)
        return f"{product_name}__{date}_{q.z}_{q.x}_{q.y}"
