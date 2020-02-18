from tifffile import imread
import os
import ee

from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import vis_s2_fire, vis_s2_firethresh, vis_s2_nbr
import matplotlib.pyplot as plt

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data_dir")

ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(
    platform="sentinel",
    sensor="2",
    product="l1c"
)


for root, dirs, files in os.walk(
        os.path.join(data_dir, "sentinel-2_l1c_manual_2019-01-01_2019-12-31_13_256x256_w_fire"), topdown=False
):
    for name in files:
        image = imread(os.path.join(root, name))

        plt.figure(0)
        out = vis_s2_fire(ee_product, image, {})
        plt.imshow(out)

        plt.figure(1)
        out = vis_s2_nbr(ee_product, image, {})
        plt.imshow(out)

        plt.figure(2)
        out = vis_s2_firethresh(ee_product, image, {})
        plt.imshow(out)

        plt.show()