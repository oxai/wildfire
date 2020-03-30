import tkinter as tk

import numpy as np
from PIL import ImageTk
from tifffile import imread

from resources.helpers import *


class Main_Panel(tk.Frame):

    def __init__(self, master, rgb_vis, ee_product=None, fonts={}, colours={}, im_size=(256, 256), vis_conf_dict=None):

        tk.Frame.__init__(self, master, bg=colours["blank"])

        self.master = master
        self.im_size = im_size
        self.cur_img_path = None
        self.cur_vis_PIL = None
        self.ee_product = ee_product
        self.rgb_vis = rgb_vis
        self.fonts = fonts
        self.colours = colours
        self.mask_pils = []

        self.vis_dict = {"RGB": rgb_vis}
        if vis_conf_dict is not None:
            for name in [n for (n, t) in self.vis_dict.keys() if t == "vis"]:
                self.vis_dict[name] = vis_conf_dict[("name", "vis")]

        self.init_topbar()

        self.topbar.pack(fill=tk.BOTH)
        self.canvas.pack()

    def init_topbar(self):
        self.topbar = tk.Frame(self, bg=self.colours["toolbar_bg"])
        self.filter_names = self.vis_dict.keys()

        self.cur_filter_name = tk.StringVar(self)
        self.cur_filter_name.set("RGB")
        self.filter_chooser = make_option_menu(master=self.topbar,
                                               variable=self.cur_filter_name,
                                               choices=self.filter_names,
                                               colours=self.colours,
                                               command=self.update_filter)

        self.filter_label = make_toolbar_label(master=self.topbar,
                                               txt="Visualiser: ",
                                               colours=self.colours)

        self.canvas = tk.Canvas(self,
                                width=self.im_size[0],
                                height=self.im_size[1],
                                bg=self.colours["canvas_bg"])

        self.cur_combi_name = tk.StringVar(self)
        self.cur_combi_name.set("update_AND_mask")

        self.combi_chooser = make_option_menu(master=self.topbar,
                                              variable=self.cur_combi_name,
                                              choices=["update_AND_mask",
                                                       "update_overlapping_masks",
                                                       "update_additive_masks"],
                                              colours=self.colours)

        self.combi_label = make_toolbar_label(master=self.topbar,
                                              txt="Combination function: ",
                                              colours=self.colours)
        self.combi_label.grid(row=0, column=0)
        self.combi_chooser.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.filter_label.grid(row=0, column=2)
        self.filter_chooser.grid(row=0, column=3, columnspan=2, sticky="ew")

    def update_vis_pil(self):
        inn = imread(self.cur_img_path)
        out = self.rgb_vis(self.ee_product, inn, {})
        out.thumbnail(self.im_size)
        self.cur_vis_PIL = out

    def update_path(self, path):
        self.cur_img_path = path
        self.update_vis_pil()
        self.rerender()

    def rerender(self):
        # TODO: can I separate this? (do I need to redraw PIL?)
        x, y = self.im_size[0] // 2, self.im_size[1] // 2,

        self.vis_im = ImageTk.PhotoImage(self.cur_vis_PIL)
        self.vis_im_sprite = self.canvas.create_image((x, y),
                                                      image=self.vis_im)
        self.overlays = []
        self.overlay_sprites = []
        for m_p in self.mask_pils:
            self.overlays.append(ImageTk.PhotoImage(m_p))
            self.overlay_sprites.append(self.canvas.create_image(self.im_size[0] // 2, self.im_size[1] // 2,
                                                                 image=self.overlays[-1]))

    def get_product_mask_pil(self, masks, colours):
        colour = np.array([0, 0, 0])
        if len(masks) > 0:
            prod_mask = masks[0]
            colour += np.array(colours[0])

        for mask, col in zip(masks[1:], colours[1:]):
            prod_mask = np.bitwise_and(mask, prod_mask)
            colour += np.array(col)
        return (render_binary_mask_as_PIL(prod_mask, colour, internal_alpha=1, im_size=self.im_size))

    def update_AND_mask(self, masks, colours):
        self.mask_pils = []
        self.mask_pils.append(self.get_product_mask_pil(masks, colours))
        self.rerender()

    def update_overlapping_masks(self, masks, colours):
        self.mask_pils = []
        for mask, colour in zip(masks, colours):
            self.mask_pils.append(render_binary_mask_as_PIL(mask, colour, im_size=self.im_size))
        self.rerender()

    def update_additive_masks(self, masks, colours):
        self.mask_pils = []
        pil = render_b_masks_as_additive_PIL(masks, colours, im_size=self.im_size)
        self.mask_pils.append(pil)
        self.rerender()

    def update_filter(self, *args):
        self.update_vis_pil()
        self.rerender()

    def update_masks(self, masks, colours):
        str = self.cur_combi_name.get()
        if str == "update_AND_mask":
            self.update_AND_mask(masks, colours)
        elif str == "update_overlapping_masks":
            self.update_overlapping_masks(masks, colours)
        elif str == "update_additive_masks":
            self.update_additive_masks(masks, colours)
        else:
            print(":(")
