import argparse
import os, requests, zipfile

from .methods import get_image_download_url_for_tile, get_ee_product
from io import BytesIO
from skimage import io
from tifffile import imsave
from skimage.transform import resize
import shutil
from .methods import TileDateRangeQuery
from resources.utils.gis import deg2tile
import matplotlib.pyplot as plt
import sys
import pandas as pd


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


def download_from_df(image_loader, df, ee_product, zoom, subdir, display=False):
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

        print(f"Downloading {i}th record. (x, y) = ({x}, {y}), {start_date} to {end_date}")

        # download images that contain wildfire
        try:
            image_loader.load(ee_product, query, subdir=subdir)
        except KeyboardInterrupt:
            sys.exit()

        print(f"Downloaded {i}th record. (x, y) = ({x}, {y}), {start_date} to {end_date}")

        if display and i % 10 == 0:
            out = image_loader.visualise(ee_product, query)
            print(out)
            print(f'Displaying {i}th downloaded image. To download without diplaying, pass "display=False".')
            plt.imshow(out)
            plt.show()


def get_parser():
    parser = argparse.ArgumentParser(description="Parse inputs")
    parser.add_argument('platform', help="satellite category ('landsat', 'sentinel', 'modis', etc.)")
    parser.add_argument('sensor', help="sensor type (landsat '8', sentinel '2', modis 'terra', etc.)")
    parser.add_argument('product', help="product name ('surface', 'ndvi', 'snow', 'temperature', etc.)")
    parser.add_argument('--from_date', help="search records after this date: yyyy-mm-dd",
                        default='2015-01-01')
    parser.add_argument('--until_date', help="search records before this date: yyyy-mm-dd",
                        default='2015-12-31')
    parser.add_argument('--bbox', '-b', metavar=('lng_left', 'lat_lower', 'lng_right', 'lat_upper'), type=float, nargs=4,
                        default=[-120, 30, -85, 45],
                        help="search records in this region: "
                             "[lng_left, lat_lower, lng_right, lat_upper]")
    parser.add_argument('--n_samples', '-n', type=int, help="number of samples", default=100)
    parser.add_argument('--min_fire_size', '-fs', type=float, help="fire size threshold", default=1000)
    parser.add_argument('--subdir_with_fire', help="directory to save images with fire", default=None)
    parser.add_argument('--subdir_no_fire', help="directory to save images without fire", default=None)
    return parser


def get_arguments():
    parser = get_parser()
    args = parser.parse_args()

    ee_product = get_ee_product(
        platform=args.platform,
        sensor=args.sensor,
        product=args.product
    )

    dir_name_base = f"{args.platform}-{args.sensor}_{args.from_date}_{args.until_date}"
    subdir_with_fire = args.subdir_with_fire
    subdir_with_fire = subdir_with_fire if subdir_with_fire else f"{dir_name_base}_w_fire"
    subdir_no_fire = args.subdir_no_fire
    subdir_no_fire = subdir_no_fire if subdir_no_fire else f"{dir_name_base}_no_fire"

    return args, ee_product, subdir_with_fire, subdir_no_fire
