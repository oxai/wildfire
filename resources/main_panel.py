import tkinter as tk

import numpy as np
from PIL import ImageTk
from tifffile import imread

from resources.helpers import *


class Main_Panel(tk.Frame):

    def __init__(self, master, rgb_vis, ee_product=None, fonts={}, colours={}, im_size=(256, 256), vis_conf_dict=None):

        tk.Frame.__init__(self,
                          master,
                          bg=colours["blank"],
                          highlightbackground=colours["toolbar_txt"],
                          highlightthickness=1)

        self.master = master
        self.im_size = im_size
        self.cur_img_path = None
        self.cur_vis_PIL = None
        self.ee_product = ee_product
        self.rgb_vis = rgb_vis
        self.fonts = fonts
        self.colours = colours
        self.cur_bin_mask = None
        self.cur_inp_bin_masks = []
        self.cur_mask_pil = None
        self.combi_func_dict = {"AND":self.get_AND_bin_mask}
        self.mask_visualisers = {"OUT_ONLY":self.get_out_only_pil}


        self.vis_dict = {"RGB": rgb_vis}
        if vis_conf_dict is not None:
            for name in [n for (n, t) in vis_conf_dict.keys() if t == "vis"]:
                self.vis_dict[name] = vis_conf_dict[(name, "vis")]

        self.init_topbar()

        self.topbar.pack(fill=tk.BOTH)
        self.canvas.pack()

    def init_topbar(self):
        self.topbar = tk.Frame(self,
                               bg=self.colours["toolbar_bg"],
                               highlightbackground=self.colours["toolbar_txt"],
                               highlightthickness=2)
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
        self.cur_combi_name.set(list(self.combi_func_dict.keys())[0])
        self.combi_chooser = make_option_menu(master=self.topbar,
                                              variable=self.cur_combi_name,
                                              choices=self.combi_func_dict.keys(),
                                              colours=self.colours)

        self.combi_label = make_toolbar_label(master=self.topbar,
                                              txt="Combination function: ",
                                              colours=self.colours)

        self.cur_mask_visualiser_name = tk.StringVar(self)
        self.cur_mask_visualiser_name.set(list(self.mask_visualisers.keys())[0])
        self.mask_vis_chooser = make_option_menu(master=self.topbar,
                                                 variable=self.cur_mask_visualiser_name,
                                                 choices=self.mask_visualisers.keys(),
                                                 colours=self.colours)
        self.mask_vis_label = make_toolbar_label(master=self.topbar,
                                                 txt="Masks visualiser: ",
                                                 colours=self.colours)


        self.combi_label.pack(side="left")
        self.combi_chooser.pack(side="left", padx=(0,32))

        self.mask_vis_label.pack(side="left")
        self.mask_vis_chooser.pack(side="left", padx=(0,32))

        self.filter_label.pack(side="left")
        self.filter_chooser.pack(side="left", padx=(0,32))

    def update_vis_pil(self):
        inn = imread(self.cur_img_path)
        vis_f = self.vis_dict[self.cur_filter_name.get()]
        out = vis_f(self.ee_product, inn, {})
        out.thumbnail(self.im_size)
        self.cur_vis_PIL = out

    def update_path(self, path):
        self.cur_img_path = path
        self.update_vis_pil()
        self.cur_mask_pil = None
        self.rerender()

    def rerender(self):
        # TODO: can I separate this? (do I need to redraw PIL?)
        x, y = self.im_size[0] // 2, self.im_size[1] // 2,

        self.vis_im = ImageTk.PhotoImage(self.cur_vis_PIL)
        self.vis_im_sprite = self.canvas.create_image((x, y),
                                                      image=self.vis_im)

        if self.cur_mask_pil != None:
            self.overlay = ImageTk.PhotoImage(self.cur_mask_pil)
            self.overlay_sprite = self.canvas.create_image(self.im_size[0] // 2,
                                                           self.im_size[1] // 2,
                                                           image=self.overlay)


    def get_AND_bin_mask(self, masks):
        if len(masks) > 0:
            prod_mask = masks[0]
        else:
            prod_mask=None

        for mask in masks[1:]:
            prod_mask = np.bitwise_and(mask, prod_mask)

        return prod_mask

    def get_out_only_pil(self, out_mask, inp_masks, inp_colours, colour=[255,255,255]):
        return render_binary_mask_as_PIL(out_mask,
                                         colour,
                                         internal_alpha=0.8,
                                         im_size=self.im_size)

    def update_filter(self, *args):
        self.update_vis_pil()
        self.rerender()

    def update_masks(self, masks, colours):
        self.cur_inp_bin_masks = masks
        bin_f = self.combi_func_dict[self.cur_combi_name.get()]
        self.cur_bin_mask = bin_f(masks)
        pil_f = self.mask_visualisers[self.cur_mask_visualiser_name.get()]
        self.cur_mask_pil = pil_f(out_mask=self.cur_bin_mask,
                                  inp_masks=masks,
                                  inp_colours=colours)
        self.rerender()

    def get_bin_mask(self, masks, colours):
        self.update_masks(masks, colours)
        return self.cur_bin_mask