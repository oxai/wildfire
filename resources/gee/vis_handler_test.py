import tifffile
import numpy as np
from .vis_handler import vis_s2_fire, vis_s2_veg, vis_s2_dnbr
import matplotlib.pyplot as plt
import ee
from .config import EE_CREDENTIALS
from .methods import get_ee_product

ee.Initialize(EE_CREDENTIALS)

ee_product = get_ee_product(platform="sentinel", sensor="2", product="l1c")
im = tifffile.imread('resources/gee/data_dir/examples/sentinel_test_img_fire.tif')
arr = np.array(im)
vis_veg_arr = vis_s2_veg(ee_product, arr, vis_params=None)
plt.imshow(vis_veg_arr)
plt.show()
vis_fire_arr = vis_s2_fire(ee_product, arr, vis_params=None)
plt.imshow(vis_fire_arr)
plt.show()
vis_dnbr_arr = vis_s2_dnbr(ee_product, arr, vis_params=None,comp_image=None)
plt.imshow(vis_dnbr_arr)
plt.show()
