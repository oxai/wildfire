import tifffile
import numpy as np
from .vis_handler import vis_fire
import matplotlib.pyplot as plt
import ee
from .config import EE_CREDENTIALS
from .methods import get_ee_product


ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(platform="sentinel",sensor="2",product="l1c")
im = tifffile.imread('resources/gee/data_dir/test_imgs/sentinel_test_img.tif')
arr = np.array(im)
vis_fire_arr = vis_fire(ee_product,arr,vis_params=None)
plt.imshow(vis_fire_arr)
plt.show()


