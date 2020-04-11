import tkinter as tk

from PIL import ImageTk
from tifffile import imread

from resources.gee.vis_handler import visualise_image
from tools.GUI_labeler.mask_helpers import *
from tools.GUI_labeler.config import colours, rgb_vis, vis_conf_dict, ee_product
from tools.GUI_labeler.tk_ui_helpers import make_option_menu, make_toolbar_label


class Product_Panel(tk.Frame):

    def __init__(self, master, im_size: (int, int) = (256, 256)):
        """
        Used to view original image and interaction of current binary masks. Also generates the combination binary mask

        :param master: the tkinter object in which this frame should be rendered
        :param im_size: the maximum size at which the image should be rendered (the frame will be larger)
        """
        tk.Frame.__init__(self,
                          master,
                          bg=colours["blank"],
                          highlightbackground=colours["toolbar_txt"],
                          highlightthickness=1)

        self.master = master
        self.im_size = im_size
        self.cur_img_path = None
        self.cur_vis_PIL = None
        self.cur_bin_mask = None
        self.cur_inp_bin_masks = []
        self.cur_mask_pil = None
        self.combi_func_dict = {"AND": get_AND_bin_mask,
                                "OR": get_OR_bin_mask}
        self.mask_visualisers = {"OUT_ONLY": self.get_out_only_pil,
                                 "MIX_COLOURS": self.get_colour_mix_pil}
        self.overlay_sprite = None
        self.overlay = None

        # vis_dict needs to be separate since RGB has no corresponding
        #  confidence mask function
        self.vis_dict = {"RGB": rgb_vis}
        if vis_conf_dict is not None:
            for pair_name in vis_conf_dict.keys():
                self.vis_dict[pair_name] = vis_conf_dict[pair_name]["vis"]

        self.init_top_bar()

        self.topbar.pack(fill=tk.BOTH)
        self.canvas.pack()

    def init_top_bar(self):
        """
        Create the top toolbar and its constituents
        """
        self.topbar = tk.Frame(self,
                               bg=colours["toolbar_bg"],
                               highlightbackground=colours["toolbar_txt"],
                               highlightthickness=2)
        self.filter_names = self.vis_dict.keys()

        self.cur_filter_name = tk.StringVar(self)
        self.cur_filter_name.set("RGB")
        self.filter_chooser = make_option_menu(master=self.topbar,
                                               variable=self.cur_filter_name,
                                               choices=self.filter_names,
                                               command=self.update_filter)

        self.filter_label = make_toolbar_label(master=self.topbar,
                                               txt="Visualiser: ")

        self.canvas = tk.Canvas(self,
                                width=self.im_size[0],
                                height=self.im_size[1],
                                bg=colours["canvas_bg"])

        self.cur_combi_name = tk.StringVar(self)
        self.cur_combi_name.set(list(self.combi_func_dict.keys())[0])
        self.combi_chooser = make_option_menu(master=self.topbar,
                                              variable=self.cur_combi_name,
                                              choices=self.combi_func_dict.keys())

        self.combi_label = make_toolbar_label(master=self.topbar,
                                              txt="Combination function: ")

        self.cur_mask_visualiser_name = tk.StringVar(self)
        self.cur_mask_visualiser_name.set(list(self.mask_visualisers.keys())[0])
        self.mask_vis_chooser = make_option_menu(master=self.topbar,
                                                 variable=self.cur_mask_visualiser_name,
                                                 choices=self.mask_visualisers.keys())
        self.mask_vis_label = make_toolbar_label(master=self.topbar,
                                                 txt="Masks visualiser: ")

        self.combi_label.pack(side="left")
        self.combi_chooser.pack(side="left", padx=(0, 32))

        self.mask_vis_label.pack(side="left")
        self.mask_vis_chooser.pack(side="left", padx=(0, 32))

        self.filter_label.pack(side="left")
        self.filter_chooser.pack(side="left", padx=(0, 32))

    def update_vis_pil(self):
        """
        Update the PIL visualising the TIF image (usually in RGB)
        """
        inn = imread(self.cur_img_path)
        vis_f = self.vis_dict[self.cur_filter_name.get()]
        out = visualise_image(inn, ee_product, handler=vis_f)
        out.thumbnail(self.im_size)
        self.cur_vis_PIL = out

    def update_path(self, path: str):
        """
        Update the path of the TIF image currently under consideration

        :param path:
        """
        self.cur_img_path = path
        self.update_vis_pil()
        self.cur_mask_pil = None
        self.rerender()

    def rerender(self):
        """
        Update canvas according to current stored PIL images
        """
        x, y = self.im_size[0] // 2, self.im_size[1] // 2,

        self.vis_im = ImageTk.PhotoImage(self.cur_vis_PIL)
        self.vis_im_sprite = self.canvas.create_image((x, y),
                                                      image=self.vis_im)

        if self.cur_mask_pil is not None:
            self.overlay = ImageTk.PhotoImage(self.cur_mask_pil)
            self.overlay_sprite = self.canvas.create_image(self.im_size[0] // 2,
                                                           self.im_size[1] // 2,
                                                           image=self.overlay)
        else:  # prevent rendering ghost masks
            self.overlay = None
            self.overlay_sprite = None

    def get_out_only_pil(self,
                         out_mask: np.ndarray,
                         inp_masks: List[np.ndarray],  # Needed for generality
                         inp_colours: List[np.ndarray],  # ^
                         colour=None) -> Image.Image:
        """
        One of the mask_visualisers options: generate a PIL depicting only the combined mask
        (and ignoring all of the masks given by the vis_panels and the combined mask)

        :param out_mask: a single binary mask of shape (w,h)
        :param inp_masks: a list of binary masks of shape (w,h)
        :param inp_colours: a list of colours to be used (if wanted) for the input masks
        :param colour: a single colour to be used as desired
        :return: a PIL representing the out_mask and/or inp_masks
        """
        if colour is None:
            colour = [255, 255, 255]
        return render_binary_mask_as_pil(out_mask,
                                         colour,
                                         internal_alpha=0.4,
                                         im_size=self.im_size)

    def get_colour_mix_pil(self,
                           out_mask: np.ndarray,
                           inp_masks: List[np.ndarray],  # Needed for generality
                           inp_colours: List[Tuple[int, int, int]],  # ^
                           colour=None) -> Image.Image:
        """
        One of the mask_visualisers options: generate a PIL depicting the input masks mixed together

        :param out_mask: a single binary mask of shape (w,h)
        :param inp_masks: a list of binary masks of shape (w,h)
        :param inp_colours: a list of colours to be used (if wanted) for the input masks
        :param colour: a single colour to be used as desired
        :return: a PIL representing the out_mask and/or inp_masks
        """
        return render_masks_as_colour_mix_pil(binary_masks=inp_masks,
                                              colours=inp_colours,
                                              im_size=self.im_size)

    def update_filter(self, *args):
        """
        To be called in the event of a change of filter

        :param args: a dummy for the OptionMenu object
        """
        self.update_vis_pil()
        self.rerender()

    def update_masks(self, masks: List[np.ndarray], inp_colours: List[List[int]]):
        """
        Updates the attributes containing binary masks. To be called when the vis_panels change

        :param masks: a list of (w,h) binary np.arrays
        :param inp_colours: a list of RGB colours to be used with the masks (in order given)
        """
        self.cur_inp_bin_masks = masks
        bin_f = self.combi_func_dict[self.cur_combi_name.get()]
        self.cur_bin_mask = bin_f(masks)
        pil_f = self.mask_visualisers[self.cur_mask_visualiser_name.get()]
        self.cur_mask_pil = pil_f(out_mask=self.cur_bin_mask,
                                  inp_masks=masks,
                                  inp_colours=inp_colours)
        self.rerender()

    def get_bin_mask(self, masks: List[np.ndarray], inp_colours: List[List[int]]) -> np.ndarray:
        """
        To be called by main window to get a binary mask to be saved

        Updates the attribute masks in case of a change

        :param masks: a list of (w,h) binary np.arrays
        :param inp_colours: a list of RGB colours to be used with the masks (in order given)
        :return: a (w,h) np.ndarray binary mask representing the combined masks
        """
        self.update_masks(masks, inp_colours)
        return self.cur_bin_mask
