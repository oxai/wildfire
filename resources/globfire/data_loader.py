import ee
import geopandas as gpd
import pandas as pd
import os
import time
from datetime import datetime, timedelta
from resources.base.data_loader import DataLoader
from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product_name, get_ee_collection_from_product, \
    get_ee_image_list_from_collection, get_ee_image_date
from resources.gee.tile_loader_helper import save_ee_image
from resources.globfire.data_loader_helper import get_arguments
import pickle


class GlobFireDataLoader(DataLoader):
    def __init__(self, subdir="MODIS_BA_GLOBAL"):
        super(GlobFireDataLoader, self).__init__()
        self.shp_dir = self.data_subdir(subdir)
        self.final = {}
        self.active = {}
        self.load()

    def load(self):
        pickle_path = os.path.join(self.data_dir(), "data.pk")
        if os.path.exists(pickle_path):
            with open(pickle_path, "rb") as f:
                self.final, self.active = pickle.load(f)
                return
        for root, dirs, files in os.walk(self.shp_dir):
            for file in files:
                if ".shp" in file:
                    year = int(file[-8:-4])
                    month = int(file.split('_')[-2])
                    key = f'{year}-{month}'
                    path = os.path.join(root, file)
                    shp = gpd.read_file(path)

                    active_area = shp[shp["Type"] == "ActiveArea"].drop(columns=['FDate'])\
                        .rename(columns={'IDate': 'Date'}).dissolve(by=['Id', 'Date'])
                    final_area = shp[shp["Type"] == "FinalArea"]
                    final_area = final_area.assign(period=final_area.apply(
                        lambda x: datetime.strptime(x['FDate'], '%Y-%m-%d') - datetime.strptime(x['IDate'], '%Y-%m-%d'),
                        axis=1))

                    self.final[key] = final_area
                    self.active[key] = active_area
        with open(pickle_path, "wb") as f:
            pickle.dump((self.final, self.active), f)

    def download(self, ee_product, min_period: int, max_period: int, save_dir=None, subdir="tmp", zoom=13, limit_sample=False):
        for _, final in self.final.items():
            df = final[
                final.apply(lambda x: timedelta(days=min_period) <= x['period'] <= timedelta(days=max_period), axis=1)
            ].reset_index()
            for _, record in df.iterrows():
                bbox = record['geometry'].bounds
                id = record['Id']
                ignition_date = record['IDate']
                finish_date = record['FDate']

                dates = pd.date_range(ignition_date, finish_date)
                print(f"Fire id: {id}, number of days: {len(dates)}")
                if limit_sample:
                    centre = len(dates) // 2
                    dates = dates[centre-2:centre+2]

                for date in dates:
                    from_date = date
                    until_date = (date + timedelta(days=1))
                    ee_collection_for_date = get_ee_collection_from_product(ee_product, bbox, from_date, until_date)
                    n_images = ee_collection_for_date.size().getInfo()
                    if n_images == 0:
                        continue
                    ee_image = ee_collection_for_date.median()
                    bands = ee_product.get('bands', [ee_product['index']])
                    image_id = self.image_id(id, ee_product, date.strftime("%Y-%m-%d"))
                    self.save(image_id, ee_image, bands, bbox, save_dir=save_dir, subdir=subdir, zoom=zoom)

    def save(self, image_id, ee_image, bands, bbox, save_dir=None, subdir="tmp", zoom=13, n_trials=3, sleep=1):
        save_dir = self.data_subdir(subdir) if save_dir is None else os.path.join(save_dir, subdir)
        base_path = os.path.join(save_dir, image_id)
        if not os.path.exists(base_path + ".tif"):
            for i in range(n_trials):
                try:
                    save_ee_image(base_path, ee_image, bands, image_id, bbox, zoom=zoom)
                    print(f"Downloaded record ({i + 1} attempt{'s' if i else ''}). Image Id: {image_id}")
                    break
                except Exception as e:
                    print(e)
                    if i == n_trials - 1:
                        print(f"Failed to download record ({i + 1} attempt{'s' if i else ''}). Image Id: {image_id}")
                        return None
                    time.sleep(sleep * 2 ** i)  # Sometimes request works on second try

    def image_id(self, globfire_id, ee_product, date: str):
        product_name = get_ee_product_name(ee_product)
        return f"{globfire_id}__{product_name}__{date}"


if __name__ == "__main__":
    args, ee_product, subdir, zoom = get_arguments()

    print("Initializing Google Earth Engine...")
    ee.Initialize(EE_CREDENTIALS)

    print("Loading GlobFire...")
    loader = GlobFireDataLoader()
    print('Loaded GlobFire')
    loader.download(ee_product, args.min_period, args.max_period, args.dir, subdir, zoom, args.limit_sample)