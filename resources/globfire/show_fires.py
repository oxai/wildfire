from tifffile import imread
import os
import argparse
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import vis_nbr, vis_firethresh, vis_fire, vis_default
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('platform', help="satellite category ('landsat', 'sentinel', 'modis', etc.)")
parser.add_argument('sensor', help="sensor type (landsat '8', sentinel '2', modis 'terra', etc.)")
parser.add_argument('product', help="product name ('surface', 'ndvi', 'snow', 'temperature', etc.)")
parser.add_argument("dir", help="tiff file directory")

args = parser.parse_args()

ee_product = get_ee_product(
    platform=args.platform,
    sensor=args.sensor,
    product=args.product
)

for root, dirs, files in os.walk(args.dir):
    for name in files:
        fig, axs = plt.subplots(1, 3)

        ax = axs[0]
        image = imread(os.path.join(root, name))
        out = vis_fire(ee_product, image, {})
        ax.imshow(out)
        ax.set_title("fire vis applied")

        ax = axs[1]
        out = vis_default(ee_product, image, ee_product['vis_params'])
        ax.imshow(out)
        ax.set_title("original RGB")

        ax = axs[2]
        out = vis_firethresh(ee_product, image, {})
        ax.imshow(out)
        ax.set_title("fire vis")

        plt.show(block=True)
