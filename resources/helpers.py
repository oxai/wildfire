import numpy as np
from PIL import Image
import tkinter as tk


def make_option_menu(master, variable, choices, colours, command=None):
    combi_chooser = tk.OptionMenu(master,
                                  variable,
                                  *choices,
                                  command=command)
    combi_chooser["fg"] = colours["toolbar_txt"]
    combi_chooser['menu'].config(bg=colours["toolbar_bg"], fg=colours["toolbar_txt"])
    combi_chooser.config(bg=colours["toolbar_bg"], bd=1)
    combi_chooser["highlightthickness"] = 0
    return combi_chooser


def make_toolbar_label(master, txt, colours):
    return tk.Label(master,
                    text=txt,
                    bg=colours["toolbar_bg"],
                    fg=colours["toolbar_txt"])


def make_toolbar_button(master, txt, command, colours):
    return tk.Button(master, text=txt,
                     command=command,
                     bg=colours["toolbar_bg"],
                     fg=colours["toolbar_txt"],
                     bd=0)


def make_menu_bar_button(master, txt, command, colours):
    return tk.Button(master, text=txt,
                     command=command,
                     bg=colours["menu_bar_bg"],
                     fg=colours["menu_bar_txt"],
                     bd=0)


def render_binary_mask_as_PIL(binary_mask, colour_rgb=[255, 0, 255], border_alpha=1, internal_alpha=0.2, im_size=None):
    assert (len(binary_mask.shape) == 2)
    if im_size == None:
        im_size = binary_mask.shape
    w, h = binary_mask.shape
    rgb_channels = [np.ones((w, h)) * v for v in colour_rgb]

    alpha_channel = highlight_borders(binary_mask * 255,
                                      border_alpha=border_alpha,
                                      internal_alpha=internal_alpha)

    ch4 = np.dstack((rgb_channels + [alpha_channel]))

    return get_pil_from_4channel(ch4, im_size)


def render_b_masks_as_additive_PIL(masks, colours, alpha=0.6, im_size=None):
    w, h = masks[0].shape

    rgb_channels = np.zeros((w, h, 3))
    for mask, col in zip(masks, colours):
        rgba = col
        rgb_channels += np.dstack(([mask * beta for beta in rgba]))

    or_bmp = np.bitwise_or.reduce(masks)

    # show_stats_about_nparray(or_bmp)

    rgba = rgb_channels + [255 * alpha * or_bmp]

    return get_pil_from_4channel(rgba, im_size)


def get_pil_from_4channel(ch4, im_size=None):
    if im_size == None:
        im_size = ch4[0].shape
    img = Image.fromarray(ch4.astype(np.uint8))
    img.thumbnail(im_size)
    return img


def highlight_borders(binary_mask, border_alpha, internal_alpha, border_width=5):
    w, h = binary_mask.shape
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


def show_stats_about_nparray(a):
    print("Shape   : " + str(a.shape))
    print("Mean    : " + str(np.mean(a, axis=(0, 1))))
    print("Variance: " + str(np.var(a)))
    print("Range   : ({}, {})".format(str(a.min()), str(a.max())))
    # print("Common  : " + str(np.argmax(np.histogram(a,bins=100))))
