import argparse
from resources.gee.methods import TileDateRangeQuery
from resources.gee.vis_handler import visualise_image_from_ee_product
from resources.manual_fire.data_loader import ManualFireDataLoader
from resources.modis_fire.data_loader import ModisFireDataLoader
from .tile_loader import GeeProductTileSeriesLoader
from resources.utils.gis import deg2tile
import matplotlib.pyplot as plt
import sys
import pandas as pd
from resources.gee.methods import get_ee_product
from resources.fpa_fod.data_loader import FpaFodDataLoader
import ee
import numpy as np
from .config import EE_CREDENTIALS
from datetime import timedelta


def get_parser():
    parser = argparse.ArgumentParser(description="Parse inputs")
    parser.add_argument('platform', help="satellite category ('landsat', 'sentinel', 'modis', etc.)")
    parser.add_argument('sensor', help="sensor type (landsat '8', sentinel '2', modis 'terra', etc.)")
    parser.add_argument('product', help="product name ('surface', 'ndvi', 'snow', 'temperature', etc.)")
    parser.add_argument('fire_record',
                        help="fire records that has latitude, longitude and time (fpa_fod / modis / manual)")
    parser.add_argument('--zoom', '-z', type=int,
                        help="zoom level (default=13: tile width 4888 m at equator)", default=None)
    parser.add_argument('--img_size', '-sz', type=int,
                        help="tile size in pixels (default=256: standard size for map display). Should be of size 2^N.",
                        default=256)
    parser.add_argument('--neg', action='store_true', help="store negative examples")
    parser.add_argument('--display', action='store_true', help="display downloaded images")
    parser.add_argument('--from_date', '-from', help="search records after this date: yyyy-mm-dd",
                        default='2015-01-01')
    parser.add_argument('--until_date', '-until', help="search records before this date: yyyy-mm-dd",
                        default='2015-12-31')
    parser.add_argument('--bbox', '-b', metavar=('lng_left', 'lat_lower', 'lng_right', 'lat_upper'), type=float,
                        nargs=4,
                        default=[-120, 30, -85, 45],
                        help="search records in this region: "
                             "[lng_left, lat_lower, lng_right, lat_upper]")
    parser.add_argument('--n_samples', '-n', type=int, help="number of samples", default=100)
    parser.add_argument('--min_fire_size', '-fs', type=float, help="fire size threshold", default=0)
    parser.add_argument('--confidence', '-c', type=float, help="confidence", default=0)
    parser.add_argument('--subdir', help="directory to save images", default=None)
    return parser


def get_arguments():
    parser = get_parser()
    args = parser.parse_args()

    ee_product = get_ee_product(
        platform=args.platform,
        sensor=args.sensor,
        product=args.product
    )

    subdir = args.subdir
    if not subdir:
        dir_name_base = f"{args.platform}-{args.sensor}_{args.product}_{args.fire_record}_" \
                        f"{args.from_date}_{args.until_date}_{args.zoom}_{args.img_size}x{args.img_size}"
        subdir = dir_name_base + ("_no_fire" if args.neg else "_w_fire")

    fire_record = args.fire_record
    if fire_record == "fpa_fod":
        fire_loader = FpaFodDataLoader()
    elif fire_record == "modis":
        fire_loader = ModisFireDataLoader()
    else:
        assert fire_record == "manual", "fire_record does not match any options"
        fire_loader = ManualFireDataLoader()

    return args, ee_product, subdir, fire_loader


def download_fire_images(fire_loader, ee_product, bbox, from_date, until_date, n_samples, subdir, pos_examples=True,
                         min_fire_size=0.0, confidence=0.0, zoom=13, img_size=256, display=True):
    if pos_examples:
        df = fire_loader.get_records_in_range(
            bbox=bbox, from_date=from_date, until_date=until_date, min_fire_size=min_fire_size,
            confidence_thresh=confidence
        ).reset_index()

        print(f"Found {len(df)} wildfire records. Downloading {min(len(df), n_samples)} records...")

        download_from_df(df[:n_samples], ee_product, zoom, subdir=subdir, img_size=img_size, display=display)

    else:
        df = fire_loader.get_neg_examples(
            bbox, from_date=from_date, until_date=until_date, n_samples=n_samples
        )

        print(f"Downloading {n_samples} negative samples...")

        download_from_df(df, ee_product, zoom, subdir=subdir, img_size=img_size, display=display)


def download_from_df(df, ee_product, zoom, subdir, img_size=256, display=False, date_margin=4):
    image_loader = GeeProductTileSeriesLoader(img_size=img_size)
    for i, record in df.iterrows():
        lat = record["LATITUDE"]
        lng = record["LONGITUDE"]

        if "DATE" in record:
            date = record["DATE"]
            delta = timedelta(days=date_margin)
            start_date, end_date = date - delta, date + delta
        else:
            start_date, end_date = record["START_DATE"], record["END_DATE"]

        start_date = start_date if start_date is not pd.NaT else None
        end_date = end_date if end_date is not pd.NaT else None

        x, y = deg2tile(lat, lng, zoom)
        query = TileDateRangeQuery(x=x, y=y, z=zoom, date_from=start_date, date_to=end_date + timedelta(days=1),
                                   reducer="median")

        print(f"Downloading {i + 1}th record. (x, y) = ({x}, {y}), {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}")

        # download images that contain wildfire
        try:
            out = image_loader.load(ee_product, query, subdir=subdir)
        except KeyboardInterrupt:
            sys.exit()

        if display:
            images = [img for img in out if img is not None]
            if images:
                image = visualise_image_from_ee_product(images[0], ee_product)
                print(f'Displaying {i + 1}th downloaded image')
                plt.imshow(image)
                plt.show()


"""
how to run the script:
positive example:
>> python -m resources.gee.download_fires landsat 8 surface fpa_fod -n 1000 -fs 10.0 -c 0.0 -sz 16
negative example:
>> python -m resources.gee.download_fires landsat 8 surface fpa_fod -n 1000 --neg -sz 16
"""
if __name__ == "__main__":
    ee.Initialize(EE_CREDENTIALS)

    args, ee_product, subdir, fire_loader = get_arguments()

    zoom = args.zoom
    if zoom is None:
        zoom = 21 - int(np.log(args.img_size) / np.log(2))

    download_fire_images(fire_loader, ee_product, bbox=args.bbox, from_date=args.from_date, until_date=args.until_date,
                         n_samples=args.n_samples, subdir=subdir, pos_examples=not args.neg,
                         zoom=zoom, img_size=args.img_size, min_fire_size=args.min_fire_size, display=args.display)
