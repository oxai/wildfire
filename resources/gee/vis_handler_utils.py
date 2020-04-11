import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


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
    if image.ndim == 3 and image.shape[0] == 1:
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


def get_empty_image(shape=(256, 256, 4)):
    image = np.zeros(shape, dtype='uint8')
    return Image.fromarray(image, 'RGBA')


def stretch(val, minval, maxval): return (val - minval) / (maxval - minval)