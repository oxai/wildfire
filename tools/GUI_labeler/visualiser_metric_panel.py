import tkinter as tk

from PIL import ImageTk
from tifffile import imread

from tools.GUI_labeler.mask_helpers import *
from tools.GUI_labeler.config import colours, ee_product, vis_conf_dict
from tools.GUI_labeler.tk_ui_helpers import make_option_menu


class Visualiser_Panel(tk.Frame):

    def __init__(self, master, total_size=(256, 256), default_filt_name=None, mask_colour=None):
        """
        A panel for displaying the output on an image a visualiser/metric pair using a variable threshold

        :param master: the tkinter object inside which this frame is rendered
        :param total_size: a pair of ints - the size at which this frame should be rendered
        :param default_filt_name: the first part of a key from vis_conf_dict - determines the initial visualiser to use
        :param mask_colour: a length 3 list or 3-tuple, determines the colour to use for visualising the binary mask
        """
        tk.Frame.__init__(self,
                          master,
                          bg=colours["toolbar_bg"],
                          highlightbackground=colours["toolbar_txt"],
                          highlightthickness=1)

        if mask_colour is None:
            mask_colour = [255, 255, 255]
        self.master = master
        self.border_width = 16
        self.im_size = (total_size[0] - self.border_width, total_size[1] - self.border_width)
        self.filter_names = vis_conf_dict.keys()
        self.cur_img_path = None
        self.cur_vis_PIL = None
        self.cur_conf_mask = None
        self.cur_conf_pil = None
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
                                         showvalue=0,
                                         command=self.update_threshold)

        self.filter_chooser.grid(row=0, column=0, sticky="w")
        self.threshold_slider.grid(row=1, column=1)
        self.canvas.grid(row=1, column=0)

    def update_vis_pil(self):
        """
        Update the attribute cur_vis_pil which stores a PIL image

        Renders a new PIL image of the current TIF file specified by cur_img_path
        Uses the current visualiser (specified by cur_filter_name) to create the image
        """
        inn = imread(self.cur_img_path)
        visualiser = vis_conf_dict[self.cur_filter_name.get()]["vis"]
        out = visualiser(ee_product, inn)
        out.thumbnail(self.im_size)
        self.cur_vis_PIL = out

    def update_conf_mask(self):
        """
        Updates the [0, 1]^w*h array of pixelwise probabilities/confidence ratings

        Uses the metric function for generating confidence masks currently specified by self.cur_filter_name to
        create an np array of values from 0-1, each element of the array represents the confidence that
        there is a fire at that pixel according to that metric
        """
        inn = imread(self.cur_img_path)
        generator = vis_conf_dict[self.cur_filter_name.get()]["conf"]
        self.cur_conf_mask = generator(ee_product, inn, {})

        if self.cur_conf_mask.min() < 0 or self.cur_conf_mask.max() > 1:
            print("""
            -------------------------
            ERROR confidence mask is not normalised!!!
            Confidence masks should contain values between 0 and 1 only
            """)

            show_stats_about_nparray(self.cur_conf_mask)
            self.cur_conf_mask -= self.cur_conf_mask.min()
            self.cur_conf_mask /= self.cur_conf_mask.max()

            print(f"""
            Attempting to normalise (please fix this)
            {self.cur_conf_mask}
            New range   : ({str(self.cur_conf_mask.min())}, {str(self.cur_conf_mask.max())})
            -------------------------
            """)

        self.update_conf_pil()

    def update_conf_pil(self):
        """
        Updates the PIL representing the confidence mask

        Takes the threshold from the slider and uses it to create a binary mask from the
        confidence mask. Then renders a PIL representing this binary mask.
        """
        self.cur_bin_mask = self.cur_conf_mask >= (self.cur_threshold.get())
        self.cur_conf_pil = render_binary_mask_as_pil(self.cur_bin_mask, colour_rgb=self.mask_colour,
                                                      im_size=self.im_size)

    def update_threshold(self, *args):
        """
        Updates the confidence mask after a change in threshold value

        :param args: - dummy args for Scale object
        """
        self.update_conf_pil()
        self.rerender()

    def update_filter(self, *args):
        """
        To be called in the event of a change of filter

        Updates the visualised image and confidence mask according to a change in filter (visualiser/metric pair)
        :param args: - a dummy
        """
        self.update_vis_pil()
        self.update_conf_mask()
        self.rerender()

    def update_path(self, path: str):
        """
        Updates the stored path to the current TIF image and rerenders new data

        :param path: The path of the TIF image to be used
        """
        self.cur_img_path = path
        self.update_vis_pil()
        self.update_conf_mask()
        self.rerender()

    def rerender(self):
        """
        Updates the canvas according to current PIL attributes
        """
        x, y = self.im_size[0] // 2, self.im_size[1] // 2,

        self.vis_im = ImageTk.PhotoImage(self.cur_vis_PIL)
        self.vis_im_sprite = self.canvas.create_image((x, y),
                                                      image=self.vis_im)

        self.conf_im = ImageTk.PhotoImage(self.cur_conf_pil)
        self.conf_im_sprite = self.canvas.create_image((x, y),
                                                       image=self.conf_im)
