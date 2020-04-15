from functools import partial
from inspect import signature
import numpy as np

from resources.gee.vis_handler_utils import get_band, get_bands_by_name, apply_palette, normalise_image, array_to_image, \
    stretch


# decorator for any vis_handler
def vis_handler_wrapper(handler):
    def process(ee_product, image, vis_params=None, comp_image=None, **kwargs):
        sig = signature(handler)
        if not vis_params:
            vis_params = ee_product.get('vis_params', {})
            if 'vis_params' in sig.parameters:
                kwargs = {**kwargs, "vis_params": vis_params}
        norm_image = normalise_image(image, vis_params)
        if comp_image is not None:
            norm_comp_image = normalise_image(comp_image, vis_params)
            kwargs = {**kwargs, "comp_image": norm_comp_image}
        out = handler(ee_product, norm_image, **kwargs)
        return array_to_image(out)

    return process


def get_vis_handler(ee_product, method='default'):
    vis_params = ee_product['vis_params']
    if method == 'default':
        return vis_default
    return vis_params['handler'][method]


@vis_handler_wrapper
def vis_default(ee_product, image, vis_params=None):
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
    return out


@vis_handler_wrapper
def vis_nbr(ee_product, image):
    nir, swir, alpha = get_bands_by_name(ee_product, image, ['NIR', 'SWIR2', 'cloud_mask'])
    level = (nir - swir) / (nir + swir + 1e-9)
    out = apply_palette(level, [
        'black', 'red', 'yellow'
    ])
    out[-1] = alpha
    return out


def get_natural_nirswirmix(blue, green, red, nir, swir2):
    return [stretch((2.1 * red + 0.5 * swir2), 0.01, 0.99), stretch((2.2 * green + 0.5 * nir), 0.01, 0.99),
            stretch(3.2 * blue, 0.01, 0.99)]


# Functions to compute the changes to image for 'some' and 'lots' fire/veg etc
def get_fire_levels(blue, green, red, nir, swir2):
    R = stretch((2.1 * red + 0.5 * swir2), 0.01, 0.99) + 1.1
    G = stretch((2.2 * green + 0.5 * nir), 0.01, 0.99)
    B = stretch(2.1 * blue, 0.01, 0.99)
    return [R, G, B], [R, G + 0.5, B]


def get_veg_levels(blue, green, red, nir, swir2):
    R = stretch((2.1 * red + 0.5 * swir2), 0.01, 0.99)
    G = stretch((2.2 * green + 0.5 * nir), 0.01, 0.99) + 0.1
    B = stretch(3.2 * blue, 0.01, 0.99)
    return np.array([R, G, B]), np.array([R * 0.7, G * 1.1, B * 1.1])


# Functions to compute masks from metrics
def get_fire_indicator(ee_product, image, sensitivity=1.0):
    swir, swir2 = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2'])
    # Increase sensitivity for more possible fires and more wrong indications
    return (swir + swir2) * sensitivity


def get_veg_indicator(ee_product, image, sensitivity=1.0):
    red, nir= get_bands_by_name(ee_product, image, ['Red', 'NIR'])
    raw = (red - nir) / (red + nir + 1e-9)
    return raw * 2 + .7  # Scale to fit 1,2 thresholds, .15-->1, .65-->2


def get_nbr_indicator(ee_product, image, sensitivity=1.0):
    nir, swir2 = get_bands_by_name(ee_product, image, ['NIR', 'SWIR2'])
    return sensitivity*(nir - swir2)/(nir + swir2 + 1e-9)


def vis_from_indicator(ind_func, l_func, comp_image=None):
    @vis_handler_wrapper
    def handler(ee_product, image, comp_image=comp_image):
        B, G, R, nir, swir, swir2 = get_bands_by_name(ee_product, image,
                                                      ['Blue', 'Green', 'Red', 'NIR', 'SWIR', 'SWIR2'])
        #ind_arrays = get_bands_by_name(ee_product, image, ind_bands)
        index = ind_func(ee_product,image)
        if comp_image is not None:
            #comp_ind_arrays = get_bands_by_name(ee_product, comp_image, ind_bands)
            comp_index = ind_func(ee_product, comp_image)
            index = index - comp_index
        some_array, lots_array = l_func(B, G, R, nir, swir2)
        no_array = get_natural_nirswirmix(B, G, R, nir, swir2)

        combined_array = np.where(index > 1.0, some_array, no_array)
        combined_array = np.where(index > 2.0, lots_array, combined_array)
        return combined_array

    return handler


def get_conf_nbr(ee_product, image):
    nir, swir, alpha = get_bands_by_name(ee_product, image, ['NIR', 'SWIR', 'cloud_mask'])
    return (nir - swir) / (nir + swir + 1e-9)


def get_conf_fire(ee_product, image):
    swir, swir2 = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2'])
    return get_fire_indicator(swir, swir2)


def get_conf_firethresh(ee_product, image):
    swir, swir2 = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2'])
    return swir + swir2 / 4


vis_veg = vis_from_indicator(ind_func=get_veg_indicator,
                             l_func=get_veg_levels,
                             comp_image=None)

vis_dndvi = vis_from_indicator(ind_func=get_veg_indicator,
                             l_func=get_veg_levels)

vis_fire = vis_from_indicator(ind_func=get_fire_indicator,
                              l_func=get_fire_levels,
                              comp_image=None)

vis_dnbr = vis_from_indicator(ind_func=partial(get_nbr_indicator,sensitivity=50),
                              l_func=get_fire_levels)


@vis_handler_wrapper
def vis_firethresh(ee_product, image):
    swir, swir2, mask = get_bands_by_name(ee_product, image, ['SWIR', 'SWIR2', 'cloud_mask'])
    out = apply_palette((swir + swir2) / 4, [
        'black', 'red', 'yellow'
    ])
    out[-1] = mask
    return out
