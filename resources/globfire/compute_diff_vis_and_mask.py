import sys

sys.path.append('.')

from resources.gee.methods import get_ee_product_from_name
from resources.gee.vis_handler import *
import numpy as np
import os
import tifffile
from collections import defaultdict
from pathlib import Path
from resources.globfire.data_loader import GlobFireDataLoader
import argparse

sys.path.remove('.')


def load_fire_images_from_dir(image_dir):
    fname_list = [fname for fname in os.listdir(image_dir) if fname.endswith(".tif") or fname.endswith(".tiff")]
    images_by_fire_id = defaultdict(lambda: defaultdict(list))

    for fname in fname_list:
        fire_id, product_name, date = GlobFireDataLoader.parse_filename(fname)
        fpath = os.path.join(image_dir, fname)
        data = tifffile.imread(fpath)
        images_by_fire_id[fire_id][product_name].append({
            "name": Path(fname).stem, "path": fpath, "data": data, "date": date
        })

    return images_by_fire_id


def compute_diff_vis_for_dir(image_dir, diff_vis_func, diff_ind_func, diff_vis_name):
    """Compute and save diff vis images for all files in directory.

    ARGS:
        image_dir: the directory containing images and .tif files
        diff_vis: the function that computes a visualizer by comparing to a past
            image
        diff_vis_name: the name of the new directory where files will be written
            and the suffix to all written files
    """
    out_vis_dir = os.path.join(image_dir, f'{diff_vis_name}_visualizations')
    if not os.path.exists(out_vis_dir): os.mkdir(out_vis_dir)
    out_ind_dir = os.path.join(image_dir, f'{diff_vis_name}')
    if not os.path.exists(out_ind_dir): os.mkdir(out_ind_dir)

    images_by_fire_id = load_fire_images_from_dir(image_dir)

    print("Fire ids:", list(images_by_fire_id.keys()))

    for fire_id, products_info in images_by_fire_id.items():
        for product_name, images_info in products_info.items():
            ee_product = get_ee_product_from_name(product_name)
            images_info = sorted(images_info, key=lambda info: info["date"])

            for image_info_prev, image_info in zip(images_info[:-1], images_info[1:]):
                print(f"Computing {diff_vis_name} for image: {image_info['name']}")

                days_since = (image_info["date"] - image_info_prev["date"]).days
                if days_since > 10:
                    continue

                out_file_base = f'{image_info["name"]}.{days_since}.{diff_vis_name}'
                out_vis_fpath = os.path.join(out_vis_dir, f"{out_file_base}.png")
                out_ind_fpath = os.path.join(out_ind_dir, f"{out_file_base}")

                arr_curr = image_info["data"]
                arr_prev = image_info_prev["data"]
                if diff_vis_func is not None:
                    diff_img = diff_vis_func(ee_product, arr_curr, vis_params=None, comp_image=arr_prev)
                    diff_img.save(out_vis_fpath)
                if diff_ind_func is not None:
                    ind_curr = diff_ind_func(ee_product, arr_curr)
                    ind_prev = diff_ind_func(ee_product, arr_prev)
                    diff_ind = ind_curr - ind_prev
                    np.save(out_ind_fpath, diff_ind)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir",
                        default="/home/oxai/GlobFire/images/sentinel-2_l1c_globfire_2015-01-01_2019-12-31_13_w_fire",
                        help="directory where images are stored for processing")
    parser.add_argument("--name",
                        default="dnbr",
                        help="name of the indicator")

    args = parser.parse_args()

    vis_ind_dict = {
        "dnbr": {"vis": vis_dnbr, "ind": get_nbr_indicator},
        "dndvi": {"vis": vis_dndvi, "ind": get_veg_indicator},
    }

    vis_ind = vis_ind_dict[args.name]

    # compute_diff_vis_for_dir(FIRE_DIR,ee_product,diff_vis_func=None,diff_mask_func=get_veg_indicator,diff_vis_name='dndvi')
    compute_diff_vis_for_dir(args.dir,
                             diff_vis_func=vis_ind["vis"], diff_ind_func=vis_ind["ind"], diff_vis_name=args.name)
