from typing import Callable
import ee
from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import *


def get_ee_session() -> dict:
    """
    Gets ee_product from Google Earth Engine
    :return: ee_product (a dict)
    """
    ee.Initialize(EE_CREDENTIALS)

    ee_product = get_ee_product(
        platform="sentinel",
        sensor="2",
        product="l1c"
    )
    return ee_product


Visualiser_Func = Callable[[dict, np.ndarray, dict], Image.Image]

ee_product = get_ee_session()

# This should specify a function for turning an np array (from tifffle.imread) into a
# 3 deep np array representing RGB channels
rgb_vis = vis_default

# Each pair of (name, "vis") and (name, "conf") should give:
#    "vis" - a function which somehow visualises a metric as an RGB image. Like rgb_vis it takes
#            an np array (from tifffle.imread) and gives a 3 deep np array representing RGB channels

#    "conf" - a function which takes the same inputs as vis but return a confidence mask - an nd.array which
#             gives pixelwise probabilities/0to1 confidence ratings as to whether there is a fire at that pixel
vis_conf_dict = {("s2_nbr", "vis"): vis_s2_nbr,
                 ("s2_nbr", "conf"): get_conf_s2_nbr,
                 ("s2_fire", "vis"): vis_s2_fire,
                 ("s2_fire", "conf"): get_conf_s2_fire,
                 ("s2_firethresh", "vis"): vis_s2_firethresh,
                 ("s2_firethresh", "conf"): get_conf_s2_firethresh,
                 ("s2_nbr2", "vis"): vis_s2_nbr,
                 ("s2_nbr2", "conf"): get_conf_s2_nbr,
                 ("s2_fire2", "vis"): vis_s2_fire,
                 ("s2_fire2", "conf"): get_conf_s2_fire,
                 ("s2_firethresh2", "vis"): vis_s2_firethresh,
                 ("s2_firethresh2", "conf"): get_conf_s2_firethresh}
# }
#

# A dictionary of colours used to keep a consistent theme
colours = {"blank": "#FFA0A0",
           "canvas_bg": "#222230",
           "button": "#FFFFFF",
           "toolbar_bg": "#000020",
           "toolbar_txt": "#D0D0D0",
           "menu_bar_txt": "#BBBBBB",
           "menu_bar_bg": "#505050"}
