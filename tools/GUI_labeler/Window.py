import os
import random
import tkinter as tk
import shutil

from tools.GUI_labeler.mask_helpers import *
from tools.GUI_labeler.config import colours, vis_conf_dict
from tools.GUI_labeler.product_panel import Product_Panel
from tools.GUI_labeler.tk_ui_helpers import make_menu_bar_button
from tools.GUI_labeler.visualiser_metric_panel import Visualiser_Panel


class Window(tk.Frame):
    def __init__(self, master, unlabeled_dir, labeled_dir, move_or_copy):
        """
        Top level class in the application, handles all components and file management

        :param master: the tkinter object in which this is rendered (should be root)
        """
        tk.Frame.__init__(self, master, bg=colours["toolbar_bg"])

        self.filter_names = vis_conf_dict.keys()
        self.mask_colours = [[255, 255, 0], [255, 0, 255], [0, 255, 255]]
        # [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
        self.main_im_size = (768, 768)
        self.max_vis_rows = 3

        self.move_or_copy = move_or_copy
        self.unlabeled_dir = unlabeled_dir
        self.labeled_dir = labeled_dir
        self.paths = None
        self.cur_img_path = None
        self.update_list_of_image_paths()

        self.product_panel = Product_Panel(master=self,
                                           im_size=self.main_im_size)

        self.vis_panels = []
        self.initialise_vis_panels()
        self.initialise_top_bar()

        self.update_prod_mask_button = make_menu_bar_button(self, "<", self.update_main_masks)

        self.topbar.grid(row=0, column=0, columnspan=3, sticky=[tk.W, tk.E])
        self.product_panel.grid(row=1, column=0, rowspan=3)
        for a0, p in enumerate(self.vis_panels):
            p.grid(row=(a0 % self.max_vis_rows) + 1, column=2 + (a0 // self.max_vis_rows))
        self.update_prod_mask_button.grid(row=2, column=1)

        self.load_random_pic()

    def initialise_top_bar(self):
        """
        Creates the top toolbar and its constituents
        """
        self.topbar = tk.Frame(self, bg=colours["menu_bar_bg"])
        self.newImageButton = make_menu_bar_button(master=self.topbar, txt="Roll",
                                                   command=self.load_random_pic)
        self.saveMaskButton = make_menu_bar_button(master=self.topbar, txt="Save mask",
                                                   command=self.save_label_image_with_mask)
        self.newImageButton.pack(side=tk.LEFT)
        self.saveMaskButton.pack(side=tk.RIGHT)

    def initialise_vis_panels(self):
        """
        Creates the side panels that each represent a visualiser/metric pair

        This should create one instance of the vis_panel object for each of the visualiser/metric pairs supplied in the
        config file. Each panel is initialised to one of these pairs but can be switched later
        """
        self.vis_panels = []

        for filt, mc in zip(self.filter_names, self.mask_colours):
            v = Visualiser_Panel(self,
                                 total_size=(self.main_im_size[0] // 3, self.main_im_size[1] // 3),
                                 default_filt_name=filt,
                                 mask_colour=mc)
            self.vis_panels.append(v)

    def update_img_path(self, path: str):
        """
        Takes the path to a TIF file and updates all app components to the new file

        :param path: A path ending in ".tif
        """
        self.cur_img_path = path
        self.master.title(path)
        self.product_panel.update_path(path)
        for p in self.vis_panels:
            p.update_path(path)

    def load_random_pic(self):
        """
        Chooses a random unlabeled image to be visualised

        Will select a TIF image from the unlabeled directory
        """
        if len(self.paths) == 0:
            raise Exception(f"No images provided in the unlabeled image directory: {self.unlabeled_dir}")

        self.cur_img_path = random.choice(self.paths)
        self.update_img_path(self.cur_img_path)

    def update_list_of_image_paths(self):
        """
        Should be called after any changes to the image directory to update the stored list of paths
        """
        if not os.path.exists(self.unlabeled_dir):
            raise Exception(f"The given directory for unlabeled images does not exist: {self.unlabeled_dir}")

        def is_unlabeled_tif(name: str):
            is_a_tif = name[-4:] == ".tif"
            is_unlabeled = name[-8:-4] != "lbld"
            return (is_a_tif and is_unlabeled)

        self.paths = [os.path.join(self.unlabeled_dir, name)
                      for name in os.listdir(self.unlabeled_dir)
                      if is_unlabeled_tif(name)]

    def update_main_masks(self):
        """
        Gives binary masks from the visualisers to the main window to create a combined mask
        """
        masks = [p.cur_bin_mask for p in self.vis_panels]
        self.product_panel.update_masks(masks, self.mask_colours)

    def save_label_image_with_mask(self):
        """
        Saves the original TIF image with an np-array binary mask and fetches a new image
        """
        filename = os.path.split(self.cur_img_path)[-1]
        if not os.path.exists(self.labeled_dir):
            os.mkdir(self.labeled_dir)

        dir_name = filename.strip(".tif")
        dest_path = os.path.join(self.labeled_dir, dir_name + ".lbld.tif")
        if self.move_or_copy == "move":
            os.rename(self.cur_img_path, dest_path)
        else:
            assert (self.move_or_copy == "copy")
            shutil.copy2(self.cur_img_path, dest_path)

        masks = [p.cur_bin_mask for p in self.vis_panels]
        b_m = self.product_panel.get_bin_mask(masks, self.mask_colours)
        np.save(os.path.join(self.labeled_dir, dir_name + ".firemask"), b_m)

        self.update_list_of_image_paths()
        self.load_random_pic()
