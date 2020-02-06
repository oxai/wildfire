import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


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
        image = np.concatenate([image, np.ones((1, 256, 256))], axis=0)
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
    out[-1] = np.where(image[0] > 0, 1, 0)
    return array_to_image(out)


def vis_nbr(nir, swir, alpha):
    level = (nir - swir) / (nir + swir + 1e-9)
    out = apply_palette(level, [
        'black', 'red', 'yellow'
    ])
    out[-1] = alpha
    return array_to_image(out)


def vis_s2_nbr(ee_product, image, vis_params):
    NIR = get_band(ee_product, image, 'B8')
    SWIR = get_band(ee_product, image, 'B12')
    return vis_nbr(NIR, SWIR, np.where(NIR > 0, 1, 0))


def vis_l8_nbr(ee_product, image, vis_params):
    NIR = get_band(ee_product, image, 'B5')
    SWIR = get_band(ee_product, image, 'B7')
    return vis_nbr(NIR, SWIR, np.where(NIR > 0, 1, 0))


# Functions to visualize wildfire, adapted from https://pierre-markuse.net/2017/08/07/visualizing-wildfires-sentinel-2-imagery-eo-browser/
def stretch(val, minval, maxval): return (val - minval) / (maxval - minval)


def vis_natural_colors(ee_product, image, vis_params):
    B2, B3, B4 = get_bands(ee_product, image, ['B2', 'B3', 'B4'])
    return [stretch(3.1 * B4, 0.05, 0.9), stretch(3 * B3, 0.05, 0.9), stretch(3.0 * B2, 0.05, 0.9)];


def vis_enhanced_natural_colors(ee_product, image, vis_params):
    B2, B3, B4, B5, B8 = get_bands(ee_product, image, ['B2', 'B3', 'B4', 'B5', 'B8'])
    return [stretch((3.1 * B4 + 0.1 * B5), 0.05, 0.9), stretch((3 * B3 + 0.15 * B8), 0.05, 0.9),
            stretch(3 * B2, 0.05, 0.9)];


def vis_nirswir_color(ee_product, image, vis_params):
    B2, B8, B12 = get_bands(ee_product, image, ['B2', 'B8', 'B12'])
    return [stretch(2.6 * B12, 0.05, 0.9), stretch(1.9 * B8, 0.05, 0.9), stretch(2.7 * B2, 0.05, 0.9)]


def vis_panband(ee_product, image, vis_params):
    B8 = get_band(ee_product, image, 'B8')
    return [stretch(B8, 0.01, 0.99), stretch(B8, 0.01, 0.99), stretch(B8, 0.01, 0.99)]


def vis_natural_nirswirmix(ee_product, image, vis_params):
    B2, B3, B4, B8, B12 = get_bands(ee_product, image, ['B2', 'B3', 'B4', 'B8', 'B12'])
    return [stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99), stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99),
            stretch(3.2 * B2, 0.01, 0.99)]


def vis_pan_tinted_green(ee_product, image, vis_params):
    B8 = get_band(ee_product, image, 'B8')
    return [B8 * 0.2, B8, B8 * 0.2]


def vis_fire10vl(ee_product, image, vis_params):
    B2, B3, B4, B8, B12 = get_bands(ee_product, image, ['B2', 'B3', 'B4', 'B8', 'B12'])
    return [stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99) + 1.1, stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99),
            stretch(2.1 * B2, 0.01, 0.99)]


def vis_fire20vl(ee_product, image, vis_params):
    B2, B3, B4, B8, B12 = get_bands(ee_product, image, ['B2', 'B3', 'B4', 'B8', 'B12'])
    return [stretch((2.1 * B4 + 0.5 * B12), 0.01, 0.99) + 1.1, stretch((2.2 * B3 + 0.5 * B8), 0.01, 0.99) + 0.5,
            stretch(2.1 * B2, 0.01, 0.99)]


def vis_s2_fire(ee_product, image, vis_params):
    sensitivity = 1.0  # Increase sensitivity for more possible fires and more wrong indications
    B11, B12 = get_bands(ee_product, image, ['B11', 'B12'])
    some_fire_bool = (B11 + B12) > (1.0 / sensitivity)
    lots_fire_bool = (B11 + B12) > (2.0 / sensitivity)
    some_fire_array = vis_fire10vl(ee_product, image, vis_params)
    lots_fire_array = vis_fire20vl(ee_product, image, vis_params)
    no_fire_array = vis_natural_nirswirmix(ee_product, image, vis_params)
    fire_array = np.where(lots_fire_bool, lots_fire_array, some_fire_array)
    combined_array = np.where(some_fire_bool, fire_array, no_fire_array)
    return array_to_image(combined_array)
