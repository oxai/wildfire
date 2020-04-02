import numpy as np
from PIL import Image
from typing import Dict, List, Tuple

"""
Converts a 2D NP array of 0s and 1s and to a PIL image that can be used as an overlay

Args:
    binary_mask (2D np array): an np array of shape (w,h) with 0,1 values

Keyword Args:
    colour_rgb (3-tuple or list): a 3-tuple of [0,255]^3 (or list)
    border_alpha (float): transparency of mask border (0 for transparent, 1 for opaque)
    internal_alpha (float): as above but for transparency of center of mask

Returns:
    a PIL image of dimensions (w,h)
        """


def render_binary_mask_as_PIL(binary_mask: np.ndarray,
                              colour_rgb: (int, int, int) = (255, 0, 255),
                              border_alpha: float = 1,
                              internal_alpha: float = 0.2,
                              im_size: (int, int) = None) -> Image:
    """
    Takes a single binary_mask and represents it as a PIL to be used as an overlay

    :param binary_mask: an np array of shape (w,h) with 0,1 values
    :param colour_rgb: a 3-tuple of [0,255]^3 (or list)
    :param border_alpha: transparency of mask border (0 for transparent, 1 for opaque)
    :param internal_alpha: as above but for transparency of center of mask
    :param im_size: the maximum size of the image to be rendered
    :return: a PIL image representing the input mask
    """
    assert (len(binary_mask.shape) == 2)
    w, h = binary_mask.shape

    if im_size is None:
        im_size = binary_mask.shape

    rgb_channels = [np.ones((w, h)) * v for v in colour_rgb]
    alpha_channel = highlight_borders(binary_mask * 255,
                                      border_alpha=border_alpha,
                                      internal_alpha=internal_alpha)

    ch4 = np.dstack((rgb_channels + [alpha_channel]))

    return get_pil_from_4channel(ch4, im_size)


def render_masks_as_colour_mix_pil(binary_masks: List[np.ndarray],
                                   colours: List[Tuple[int, int, int]],
                                   border_alpha: float = 1,
                                   internal_alpha: float = 0.2,
                                   im_size: (int, int) = None) -> Image:
    """
    Takes a single binary_mask and represents it as a PIL to be used as an overlay

    :param binary_masks: a list of np arrays of shape (w,h) with 0,1 values
    :param colours: list of 3-tuples of [0,255]^3 (or list)
    :param border_alpha: transparency of mask border (0 for transparent, 1 for opaque)
    :param internal_alpha: as above but for transparency of center of mask
    :param im_size: the maximum size of the image to be rendered
    :return: a PIL image representing the a combination of the masks
    """
    n = len(binary_masks)
    (w, h) = binary_masks[0].shape
    colours4 = []
    for (r, g, b) in colours:
        total = r + g + b
        ratio = total / n
        rgba = (int(r * ratio), int(g * ratio), int(b * ratio), 255 // n)
        print(rgba)
        colours4.append(rgba)

    combi = np.zeros((w, h, 4))
    for mask, (r, g, b, a) in zip(binary_masks, colours4):
        print(mask.reshape((w, h, 1)) * np.array([[[r, g, b, a]]]))
        print((mask.reshape((w, h, 1)) * np.array([[[r, g, b, a]]])).shape)
        combi += mask.reshape((w, h, 1)) * np.array([[[r, g, b, a]]])

    return get_pil_from_4channel(ch4=combi, im_size=im_size)


def get_pil_from_4channel(ch4: List[np.ndarray],
                          im_size: (int, int) = None) -> Image:
    """
    Generates a PIL from a (w,h,4) nparray using values as RGBA channels
    :param ch4:
    :param im_size:
    :return: a PIL image
    """
    if im_size == None:
        im_size = ch4[0].shape
    img = Image.fromarray(ch4.astype(np.uint8))
    img.thumbnail(im_size)
    return img


def highlight_borders(binary_mask: np.ndarray,
                      border_alpha: float,
                      internal_alpha: float,
                      border_width: int = None) -> np.ndarray:
    """
    Takes a binary mask and returns a [0,1]*(w,h) array representing pixelwise transparency

    Used to make the internal more transparent than the bright borders
    :param binary_mask: a (w,h) np array of 0s and 1s
    :param border_alpha: a float in [0,1] representing the transparency of borders (0 transparent -> 1 opaque)
    :param internal_alpha: as above but for transparency of internal/body of mask
    :param border_width: Can specify the number of pixels in the border (else inferred from size)
    :return:
    """
    w, h = binary_mask.shape
    if border_width is None:
        border_width = (w + h) // 256
    left_filt = np.concatenate((np.zeros((w, border_width)), binary_mask[:, :-border_width]), axis=1)

    right_filt = np.concatenate((binary_mask[:, border_width:], np.zeros((w, border_width))), axis=1)

    up_filt = np.concatenate((np.zeros((border_width, h)), binary_mask[:-border_width, :]), axis=0)

    down_filt = np.concatenate((binary_mask[border_width:, :], np.zeros((border_width, h))), axis=0)

    def check_edge(a1, a2):
        return np.bitwise_and(a1.astype(int), np.bitwise_not(a2.astype(int)))

    edge_layers = [check_edge(binary_mask, f) for f in [left_filt, right_filt, down_filt, up_filt]]
    edges = edge_layers[0]
    for l in edge_layers[1:]:
        edges = np.bitwise_or(edges, l)

    return np.maximum((binary_mask * internal_alpha), (edges * border_alpha))


def show_stats_about_nparray(a: np.ndarray):
    """
    Used for bug fixing, displays some statistics about a np array
    :param a: and np.array to be learny about
    """
    print("Shape   : " + str(a.shape))
    print("Mean    : " + str(np.mean(a, axis=(0, 1))))
    print("Variance: " + str(np.var(a)))
    print("Range   : ({}, {})".format(str(a.min()), str(a.max())))
