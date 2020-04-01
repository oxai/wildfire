import tkinter as tk
from tkinter.font import Font
import numpy as np

import ee
import os
import random

from resources.main_panel import Main_Panel
from resources.visualiser_metric_panel import Visualiser_Panel
from resources.helpers import *

from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import get_visualisers_and_conf

root = tk.Tk()

colours = {"blank": "#FFA0A0",
           "canvas_bg": "#222230",
           "button": "#FFFFFF",
           "toolbar_bg": "#000020",
           "toolbar_txt": "#D0D0D0",
           "menu_bar_txt": "#BBBBBB",
           "menu_bar_bg": "#505050"}
fonts = {"small": Font(size=8)}


def get_ee_session():
    ee.Initialize(EE_CREDENTIALS)

    ee_product = get_ee_product(
        platform="sentinel",
        sensor="2",
        product="l1c"
    )
    return ee_product


class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=colours["toolbar_bg"])

        self.rgb_vis, self.vd = get_visualisers_and_conf()
        self.ee_product = get_ee_session()
        self.filter_names = [n for (n, t) in self.vd.keys() if t == "vis"]
        self.mask_colours = [[255, 255, 0], [255, 0, 255], [0, 255, 255]]
        self.main_im_size = (768, 768)

        self.base_dir = 'resources/temp-for-tool/'
        self.unlabeled_dir = self.base_dir + "unlabeled/"
        self.labeled_dir = self.base_dir + "labeled/"
        self.paths = None
        self.update_list_of_image_paths()

        self.rgb_panel = Main_Panel(master=self,
                                    rgb_vis=self.rgb_vis,
                                    ee_product=self.ee_product,
                                    fonts=fonts,
                                    im_size=self.main_im_size,
                                    colours=colours,
                                    vis_conf_dict=self.vd)

        self.vis_panels = []
        self.initialise_vis_panels()
        self.initialise_topbar()

        self.topbar.grid(row=0, column=0, columnspan=2, sticky=[tk.W, tk.E])
        self.rgb_panel.grid(row=1, column=0, rowspan=3)
        for a0, p in enumerate(self.vis_panels):
            p.grid(row=a0 + 1, column=1)

        self.load_random_pic()

    def initialise_topbar(self):
        self.topbar = tk.Frame(self, bg=colours["menu_bar_bg"])
        self.newImageButton = make_menu_bar_button(master=self.topbar,
                                                   txt="Roll",
                                                   command=self.load_random_pic,
                                                   colours=colours)
        self.saveMaskButton = make_menu_bar_button(master=self.topbar,
                                                   txt="Save mask",
                                                   command=self.save_label_image_with_mask,
                                                   colours=colours)
        self.newImageButton.pack(side=tk.LEFT)
        self.saveMaskButton.pack(side=tk.RIGHT)

    def initialise_vis_panels(self):
        self.vis_panels = []

        for filt, mc in zip(self.filter_names, self.mask_colours):
            print(filt)
            v = Visualiser_Panel(self,
                                 ee_product=self.ee_product,
                                 fonts=fonts,
                                 colours=colours,
                                 vis_conf_dict=self.vd,
                                 total_size=(self.main_im_size[0] // 3, self.main_im_size[1] // 3),
                                 default_filt_name=filt,
                                 mask_colour=mc)
            self.vis_panels.append(v)

    def update_img_path(self, path):
        self.cur_img_path = path
        self.rgb_panel.update_path(path)
        for p in self.vis_panels: p.update_path(path)

    def load_random_pic(self):
        self.cur_img_path = random.choice(self.paths)
        self.update_img_path(self.cur_img_path)

    def update_list_of_image_paths(self):
        self.paths = [self.unlabeled_dir + name for name in os.listdir(self.unlabeled_dir)]

    def update_main_masks(self):
        masks = [p.cur_bin_mask for p in self.vis_panels]
        self.rgb_panel.update_masks(masks, self.mask_colours)

    def save_label_image_with_mask(self):

        filename = os.path.split(self.cur_img_path)[-1]
        if not os.path.exists(self.labeled_dir):
            os.mkdir(self.labeled_dir)

        dir_name = filename.strip(".tif")
        assert(not os.path.exists(self.labeled_dir + dir_name + "/"))
        os.rename(self.cur_img_path, self.labeled_dir + dir_name + "img.tif")

        masks = [p.cur_bin_mask for p in self.vis_panels]
        b_m = self.rgb_panel.get_bin_mask(masks, self.mask_colours)
        np.save(self.labeled_dir + dir_name + "mask.npy", b_m)

        self.load_random_pic()
        self.update_list_of_image_paths()



def main():
    app = Window()

    def b1(event):
        if event.char == "r":
            app.update_main_masks()

    root.bind("<Key>", b1)
    root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

    app.pack()
    root.mainloop()
