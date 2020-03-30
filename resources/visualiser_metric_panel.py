import numpy as np
import tkinter as tk
from PIL import ImageTk
from tifffile import imread

from resources.helpers import *


class Visualiser_Panel(tk.Frame):

    def __init__(self, master, ee_product=None, fonts={}, colours={}, total_size=(256, 256),
                 vis_conf_dict={("NONE", "vis"): None}, default_filt_name=None, mask_colour=[255, 255, 255]):

        tk.Frame.__init__(self,
                          master,
                          bg=colours["toolbar_bg"],
                          highlightbackground=colours["toolbar_txt"],
                          highlightthickness=1)

        self.master = master
        self.border_width = 16
        self.im_size = (total_size[0] - self.border_width, total_size[1] - self.border_width)
        self.vis_conf_dict = vis_conf_dict
        self.filter_names = [n for (n, t) in vis_conf_dict.keys() if t == "vis"]
        self.cur_img_path = None
        self.cur_vis_PIL = None
        self.cur_conf_mask = None
        self.cur_conf_pil = None
        self.ee_product = ee_product
        self.fonts = fonts
        self.colours = colours
        self.mask_colour = mask_colour

        if default_filt_name is not None:
            assert (default_filt_name in self.filter_names)
        else:
            default_filt_name = self.filter_names[0]

        self.canvas = tk.Canvas(self,
                                width=self.im_size[0],
                                height=self.im_size[1],
                                bg=colours["canvas_bg"])

        self.cur_filter_name = tk.StringVar(self)
        self.cur_filter_name.set(default_filt_name)
        self.filter_chooser = make_option_menu(master=self,
                                               variable=self.cur_filter_name,
                                               choices=self.filter_names,
                                               colours=self.colours,
                                               command=self.update_filter)
        self.filter_chooser.pack(side=tk.BOTTOM)

        self.cur_threshold = tk.DoubleVar(self)
        self.cur_threshold.set("100")
        self.threshold_slider = tk.Scale(self,
                                         variable=self.cur_threshold,
                                         from_=1,
                                         to_=0,
                                         resolution=0.01,
                                         length=self.im_size[1],
                                         font=fonts["small"],
                                         showvalue=0,
                                         command=self.update_threshold)

        self.filter_chooser.grid(row=0, column=0, sticky="w")
        self.threshold_slider.grid(row=1, column=1)
        self.canvas.grid(row=1, column=0)

    def update_vis_pil(self):
        inn = imread(self.cur_img_path)
        visualiser = self.vis_conf_dict[(self.cur_filter_name.get(), "vis")]
        out = visualiser(self.ee_product, inn, {})
        out.thumbnail(self.im_size)
        self.cur_vis_PIL = out

    def update_conf_mask(self):
        inn = imread(self.cur_img_path)
        generator = self.vis_conf_dict[(self.cur_filter_name.get(), "conf")]
        self.cur_conf_mask = generator(self.ee_product, inn, {})

        if self.cur_conf_mask.min() < 0 or self.cur_conf_mask.max() > 1:
            print()
            print("-------------------------")
            print("ERROR confidence mask is not normalised!!!")
            show_stats_about_nparray(self.cur_conf_mask)
            print()
            print("automagically normalising (plz fix)")
            self.cur_conf_mask -= self.cur_conf_mask.min()
            self.cur_conf_mask /= self.cur_conf_mask.max()
            print(self.cur_conf_mask)
            print("New range   : ({}, {})".format(str(self.cur_conf_mask.min()), str(self.cur_conf_mask.max())))
            print("-------------------------")
            print()

        self.update_conf_pil()

    def update_conf_pil(self):
        self.cur_bin_mask = self.cur_conf_mask >= (self.cur_threshold.get())
        self.cur_conf_pil = render_binary_mask_as_PIL(self.cur_bin_mask, colour_rgb=self.mask_colour,
                                                      im_size=self.im_size)

    def update_threshold(self, *args):
        self.update_conf_pil()
        self.rerender()

    def update_filter(self, *args):
        self.update_vis_pil()
        self.update_conf_mask()
        self.rerender()

    def update_path(self, path):
        self.cur_img_path = path
        self.update_vis_pil()
        self.update_conf_mask()
        self.rerender()

    def rerender(self):
        # TODO: can I separate this? (do I need to redraw PIL?)

        x, y = self.im_size[0] // 2, self.im_size[1] // 2,

        self.vis_im = ImageTk.PhotoImage(self.cur_vis_PIL)
        self.vis_im_sprite = self.canvas.create_image((x, y),
                                                      image=self.vis_im)

        self.conf_im = ImageTk.PhotoImage(self.cur_conf_pil)
        self.conf_im_sprite = self.canvas.create_image((x, y),
                                                       image=self.conf_im)
