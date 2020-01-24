import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def get_vis_handler(ee_product, method='default'):
    vis_params = ee_product['vis_params']
    if method == 'default':
        return vis_default
    return vis_params['handler'][method]


def get_band(ee_product, image, band):
    return image[ee_product['bands'].index(band)]


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
    image = (image * 255).astype('uint8').transpose(1, 2, 0)
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

