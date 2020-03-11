from tifffile import imread
import os
import ee
import argparse
from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import vis_s2_fire, vis_s2_firethresh, vis_s2_nbr, vis_default
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("dir", help="tiff file directory")

args = parser.parse_args()

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", args.dir)

ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(
    platform="sentinel",
    sensor="2",
    product="l1c"
)

for root, dirs, files in os.walk(data_dir, topdown=False):
    for name in files:
        fig, axs = plt.subplots(1, 3)

        image = imread(os.path.join(root, name))
        out = vis_s2_fire(ee_product, image, {})
        axs[0].imshow(out)

        out = vis_default(ee_product, image, ee_product['vis_params'])
        axs[1].imshow(out)

        out = vis_s2_firethresh(ee_product, image, {})
        axs[2].imshow(out)

        plt.show()