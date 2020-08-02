import os
import glob
import numpy as np
from PIL import Image
import math

from resources.gee.vis_handler_utils import array_to_image


def find_precomputed_feature_path(vis_name, cur_img_path, visualise=False):
    root_dir = os.path.join(os.path.dirname(cur_img_path))
    image_id = os.path.basename(cur_img_path).split(".")[0]
    search_path = os.path.join(root_dir, vis_name + ('_vis' if visualise else '_ind'), f'{image_id}**')
    print(search_path)
    image_paths = glob.glob(search_path)
    assert len(image_paths) <= 1, f"More than one matching precomputed {vis_name} features for {cur_img_path}"
    return image_paths[0] if image_paths else None


def load_precomputed_ind(vis_name, cur_img_path):
    image_path = find_precomputed_feature_path(vis_name, cur_img_path, visualise=False)
    if image_path: return np.load(image_path)
    print(f"Could not find precomputed indicator for {vis_name}")
    return np.zeros((512, 512))


def make_orange_tile(error_size=(512, 512)):
    tile_w = 64
    tile = ([([1] * tile_w) + [0] * tile_w] * tile_w) + ([([0] * tile_w) + [1] * tile_w] * tile_w)
    reps = (math.ceil(error_size[0] / tile_w), math.ceil(error_size[1] / tile_w))
    conf_mask = np.tile(tile, reps)
    RGBA = [1, 0.5, 0, 1]
    ar = np.array([conf_mask * band for band in RGBA])
    return array_to_image(ar)


def load_precomputed_vis(vis_name, cur_img_path):

    image_path = find_precomputed_feature_path(vis_name, cur_img_path, visualise=True)
    if image_path:
        return Image.open(image_path)
    print(f"Could not find precomputed indicator for {vis_name}")
    return make_orange_tile()

