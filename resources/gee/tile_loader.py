from resources.base.data_loader import DataLoader
from .methods import get_ee_image_from_product, get_ee_product_name, get_ee_collection_from_product, get_ee_image_date, \
    get_ee_image_list_from_collection
import os
from tifffile import imread
from .tile_loader_helper import TileDateRangeQuery, save_gee_tile
from .vis_handler import get_vis_handler
from datetime import timedelta
import pandas as pd
import time


class GeeImageTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.img_size = img_size

    def save(self, image_id, ee_image, bands, query: TileDateRangeQuery, subdir="tmp", n_trials=3, sleep=1):
        base_path = os.path.join(self.data_subdir(subdir), image_id)
        if not os.path.exists(base_path+".tif"):
            # if not ee_image.bandNames().getInfo():
            #     print("No bands in image")
            #     return None
            for i in range(n_trials):
                try:
                    save_gee_tile(base_path, ee_image, bands, query, image_id, self.img_size)
                    print(f"Downloaded record ({i+1} attempt{'s' if i else ''}). Image Id: {image_id}")
                    break
                except Exception as e:
                    print(e)
                    if i == n_trials - 1:
                        print(f"Failed to download record ({i+1} attempt{'s' if i else ''}). Image Id: {image_id}")
                        return None
                    time.sleep(sleep * 2**i)  # Sometimes request works on second try
        return base_path+".tif"

    def load(self, image_id, query: TileDateRangeQuery, subdir="tmp"):
        path = os.path.join(self.data_subdir(subdir), image_id + ".tif")
        img = imread(path)
        return img


class GeeProductTileLoader(DataLoader):
    def __init__(self, img_size=256):
        super().__init__()
        self.image_loader = GeeImageTileLoader(img_size=img_size)

    def save(self, ee_product, query: TileDateRangeQuery, subdir="tmp", n_trials=3, sleep=1):
        image_id = self.image_id(ee_product, query)
        ee_image = get_ee_image_from_product(ee_product, query)
        bands = ee_product.get('bands', [ee_product['index']])
        return self.image_loader.save(image_id, ee_image, bands, query, subdir=subdir, n_trials=n_trials, sleep=sleep)

    def load(self, ee_product, query: TileDateRangeQuery, subdir="tmp"):
        path = self.save(ee_product, query, subdir=subdir)
        return imread(path) if path else None

    def image_id(self, ee_product, q: TileDateRangeQuery):
        product_name = get_ee_product_name(ee_product)
        sz = self.image_loader.img_size
        return f"{product_name}__{q.date_from}_{q.date_to}_{q.reducer}_{q.z}_{q.x}_{q.y}_{sz}x{sz}"


class GeeProductTileSeriesLoader(GeeProductTileLoader):
    def __init__(self, img_size=256):
        super(GeeProductTileSeriesLoader, self).__init__(img_size=img_size)

    def save(self, ee_product, q: TileDateRangeQuery, subdir="tmp", n_trials=3, sleep=1):
        paths = []
        ee_collection = get_ee_collection_from_product(ee_product, q)
        ee_images = get_ee_image_list_from_collection(ee_collection)
        dates = [get_ee_image_date(ee_image) for ee_image in ee_images]
        for date in pd.date_range(q.date_from, q.date_to):
            if date.strftime("%Y-%m-%d") in dates:
                query = TileDateRangeQuery(
                    x=q.x, y=q.y, z=q.z, reducer=q.reducer,
                    date_from=date.strftime("%Y-%m-%d"),
                    date_to=(date + timedelta(days=1)).strftime("%Y-%m-%d")
                )
                path = super().save(ee_product, query, subdir=subdir, n_trials=n_trials, sleep=sleep)
            else:
                path = None
            paths.append(path)
        return paths

    def load(self, ee_product, q: TileDateRangeQuery, subdir="tmp", n_trials=3, sleep=1):
        paths = self.save(ee_product, q, subdir=subdir, n_trials=n_trials, sleep=sleep)
        return [imread(path) if path else None for path in paths]

    def image_id(self, ee_product, q: TileDateRangeQuery):
        product_name = get_ee_product_name(ee_product)
        sz = self.image_loader.img_size
        return f"{product_name}__{q.date_from}_{q.z}_{q.x}_{q.y}_{sz}x{sz}"
