import argparse
from resources.gee.methods import TileDateRangeQuery
from resources.gee.vis_handler import visualise_image_from_ee_product
from .tile_loader import GeeProductTileSeriesLoader
from resources.utils.gis import deg2tile
import matplotlib.pyplot as plt
import sys
import pandas as pd
from resources.gee.methods import get_ee_product
from datetime import timedelta


def download_from_df(df, ee_product, zoom, subdir, img_size=256, display=False):
    image_loader = GeeProductTileSeriesLoader(img_size=img_size)
    for i, record in df.iterrows():
        lat = record["LATITUDE"]
        lng = record["LONGITUDE"]
        start_date = record["START_DATE"]
        end_date = record["END_DATE"]

        start_date = start_date if start_date is not pd.NaT else None
        end_date = end_date if end_date is not pd.NaT else None

        x, y = deg2tile(lat, lng, zoom)
        query = TileDateRangeQuery(x=x, y=y, z=zoom, date_from=start_date, date_to=end_date + timedelta(days=1),
                                   reducer="median")

        print(f"Downloading {i+1}th record. (x, y) = ({x}, {y}), {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}")

        # download images that contain wildfire
        try:
            out = image_loader.load(ee_product, query, subdir=subdir)
        except KeyboardInterrupt:
            sys.exit()

        if display:
            images = [img for img in out if img is not None]
            if images:
                image = visualise_image_from_ee_product(images[0], ee_product)
                print(f'Displaying {i+1}th downloaded image')
                plt.imshow(image)
                plt.show()


def get_parser():
    parser = argparse.ArgumentParser(description="Parse inputs")
    parser.add_argument('platform', help="satellite category ('landsat', 'sentinel', 'modis', etc.)")
    parser.add_argument('sensor', help="sensor type (landsat '8', sentinel '2', modis 'terra', etc.)")
    parser.add_argument('product', help="product name ('surface', 'ndvi', 'snow', 'temperature', etc.)")
    parser.add_argument('--zoom', '-z', type=int,
                        help="zoom level (default=13: tile width 4888 m at equator)", default=13)
    parser.add_argument('--img_size', '-sz', type=int,
                        help="tile size in pixels (default=256: standard size for map display)", default=256)
    parser.add_argument('--neg', action='store_true', help="store negative examples")
    parser.add_argument('--display', action='store_true', help="display downloaded images")
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
        dir_name_base = f"{args.platform}-{args.sensor}_{args.from_date}_{args.until_date}" \
                        f"_{args.zoom}_{args.img_size}x{args.img_size}"
        subdir = dir_name_base + ("_no_fire" if args.neg else "_w_fire")

    return args, ee_product, subdir
