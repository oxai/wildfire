import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import functools


def get_empty_image(shape=(256, 256, 4)):
    image = np.zeros(shape, dtype='uint8')
    return Image.fromarray(image, 'RGBA')


def visualise_image_from_ee_product(image: np.ndarray, ee_product, vis_params=None, method='default'):
    handler = get_vis_handler(ee_product, method=method)
    if not vis_params:
        vis_params = ee_product.get('vis_params', {})
    out = handler(ee_product, image, vis_params)
    return out


def get_vis_handler(ee_product, method='default'):
    vis_params = ee_product['vis_params']
    if method == 'default':
        return vis_default
    return vis_params['handler'][method]


def get_band(ee_product, image, band):
    return image[ee_product['bands'].index(band)]


def get_bands_by_name(ee_product, image, band_names):
    band_map = ee_product['band_map']
    band_numbers = [band_map[band_name] for band_name in band_names]
    return get_bands(ee_product, image, band_numbers)


def get_bands(ee_product, image, bands):
    return [get_band(ee_product, image, band) for band in bands]


def hex_color_to_num(hex):
    return tuple(int(hex[i:i + 2], 16) / 255 for i in (0, 2, 4))


popular_colors = {
    'black': "000000",
    'blue': "0000FF",
    'purple': "9F00C5",
    'cyan': "00B7EB",
    'green': "00FF00",
    'yellow': "FFFF00",
    'orange': "FFA500",
    'red': "FF0000"
}


def create_cdict(palette):
    cmap = []
    for val, color in zip(np.linspace(0, 1, len(palette)), palette):
        if color in popular_colors.keys():
            color = popular_colors[color]
        R, G, B = hex_color_to_num(color)
        cmap.append(
            ((val, R, R), (val, G, G), (val, B, B))
        )
    return dict(zip(['red', 'green', 'blue'], zip(*cmap)))


def apply_palette(image, palette):
    if image.ndim == 3:
        image = image[0]
    if isinstance(palette, list):
        cm = LinearSegmentedColormap('custom', create_cdict(palette))
    else:
        # Get the color map by name:
        cm = plt.get_cmap(palette)
    # Apply the colormap like a function to any array:
    out = cm(image)
    return out.transpose(2, 0, 1)


def normalise_image(image, vis_params):
    min_val = vis_params.get('min', 0)
    max_val = vis_params.get('max', 1)
    gamma = vis_params.get('gamma', 1)
    img = np.where(image > min_val, image, min_val)
    img = np.where(img < max_val, img, max_val)
    img = (img - min_val) / (max_val - min_val)
    img = img ** (1 / gamma)
    return img


def array_to_image(image):
    if image.shape[0] == 3:
        image = np.concatenate([image, np.ones((1, image.shape[1], image.shape[2]))], axis=0)
    image = (image.clip(0, 1) * 255).astype('uint8').transpose(1, 2, 0)
    return Image.fromarray(image, 'RGBA')


def vis_default(ee_product, image, vis_params):
    image = normalise_image(image, vis_params)
    bands = vis_params.get('bands', None)
    if bands:
        _, h, w = image.shape
        out = np.zeros((4, h, w))
        for i, band in enumerate(bands):
            out[i] = get_band(ee_product, image, band)
    else:
        palette = vis_params.get('palette', None)
        out = apply_palette(image, palette)
    if vis_params.get('alpha', True):
        if bands and 'cloud_mask' in bands:
            out[-1] = get_band(ee_product, image, 'cloud_mask')
        else:
            out[-1] = np.where(image.sum(axis=0) > 0, 1, 0)
    else:
        out[-1] = 1
    return array_to_image(out)


def vis_nbr(ee_product, image, vis_params):
    nir, swir, alpha = get_bands_by_name(ee_product, image, ['NIR', 'SWIR2', 'cloud_mask'])
    level = (nir - swir) / (nir + swir + 1e-9)
    out = apply_palette(level, [
        'black', 'red', 'yellow'
    ])
    out[-1] = alpha
    return array_to_image(out)


def stretch(val, minval, maxval): return (val - minval) / (maxval - minval)


def vis_natural_nirswirmix(B2, B3, B4, B8, B12):
    return [stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99), stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99),
            stretch(3.2 * B2, 0.01, 0.99)]


# Functions to compute the changes to image for 'some' and 'lots' fire/veg etc
def get_fire_levels(B2, B3, B4, B8, B12):
    R = stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99) + 1.1
    G = stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99)
    B = stretch(2.1 * B2, 0.01, 0.99)
    return [R, G, B], [R, G + 0.5, B]

def get_veg_levels(B2, B3, B4, B8, B12):
    R = stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99)
    G = stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99) + 0.1
    B = stretch(3.2 * B2, 0.01, 0.99)
    return np.array([R, G, B]), np.array([R*0.7, G*1.1, B*1.1])

def get_veg_levels(B2, B3, B4, B8, B12):
    R = stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99)
    G = stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99) + 0.1
    B = stretch(3.2 * B2, 0.01, 0.99)
    return np.array([R, G, B]), np.array([R*0.7, G*1.1, B*1.1])


# Functions to compute masks from metrics
def get_fire_indicator(B11, B12, sensitivity=1.0):
    # Increase sensitivity for more possible fires and more wrong indications
    return (B11 + B12) * sensitivity

def get_veg_indicator(B4, B8):
    raw = (B4 - B8)/(B4 + B8)
    return raw*2 + .7 # Scale to fit 1,2 thresholds, .15-->1, .65-->2

def get_nbr_indicator(B8, B12):
    return (B8 - B12)/(B8 + B12 + 1e-9)

def get_veg_indicator(B4, B8):
    raw = (B4 - B8)/(B4 + B8)
    return raw*2 + .7 # Scale to fit 1,2 thresholds, .15-->1, .65-->2

def get_nbr_indicator(B8, B12):
    return (B8 - B12)/(B8 + B12 + 1e-9)



def vis_from_indicator(ee_product, image, vis_params, ind_func, ind_bands, l_func, comp_image):
    B, G, R, NIR, SWIR, SWIRa = get_bands_by_name(ee_product, image, ['Blue', 'Green', 'Red', 'NIR', 'SWIR', 'SWIR2'])
    ind_arrays = get_bands_by_name(ee_product, image, ind_bands)
    index = ind_func(*ind_arrays)
    if comp_image != None:
        comp_ind_arrays = get_bands_by_name(ee_product, comp_image, ind_bands)
        comp_index = ind_func(*comp_ind_arrays)
        index = index - comp_index
    some_array, lots_array = l_func(B, G, R, NIR, SWIRa)
    no_array = vis_natural_nirswirmix(B, G, R, NIR, SWIRa)

    combined_array = np.where(index > 1.0, some_array, no_array)
    combined_array = np.where(index > 2.0, lots_array, combined_array)
    return array_to_image(combined_array)


def get_conf_nbr(ee_product, image, vis_params):
    nir, swir, alpha = get_bands_by_name(ee_product, image, ['NIR', 'SWIR', 'cloud_mask'])
    return (nir - swir) / (nir + swir + 1e-9)

def get_conf_fire(ee_product, image, vis_params):
    swir, swir2 = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2'])
    return get_fire_indicator(swir, swir2)

def get_conf_firethresh(ee_product, image, vis_params):
    swir, swir2 = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2'])
    return swir + swir2 / 4


vis_veg = functools.partial(
    vis_from_indicator,
    ind_func=get_veg_indicator,
    ind_bands = ['Red','NIR'],
    l_func = get_veg_levels,
    comp_image=None)


vis_fire = functools.partial(
    vis_from_indicator,
    ind_func=get_fire_indicator,
    ind_bands = ['SWIR','SWIR2'],
    l_func = get_fire_levels,
    comp_image=None)


vis_dnbr = functools.partial(
    vis_from_indicator,
    ind_func=get_nbr_indicator,
    ind_bands = ['SWIR','SWIR2'],
    l_func = get_fire_levels)

vis_veg = functools.partial(
    vis_from_indicator,
    ind_func=get_veg_indicator,
    ind_bands = ['Red','NIR'],
    l_func = get_veg_levels,
    comp_image=None)


vis_fire = functools.partial(
    vis_from_indicator,
    ind_func=get_fire_indicator,
    ind_bands = ['SWIR','SWIR2'],
    l_func = get_fire_levels,
    comp_image=None)


vis_dnbr = functools.partial(
    vis_from_indicator,
    ind_func=get_nbr_indicator,
    ind_bands = ['SWIR','SWIR2'],
    l_func = get_fire_levels)


def vis_firethresh(ee_product, image, vis_params):
    swir, swir2, mask = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2', 'cloud_mask'])
    out = apply_palette((swir + swir2) / 4, [
        'black', 'red', 'yellow'
    ])
    out[-1] = mask
    return array_to_image(out)
