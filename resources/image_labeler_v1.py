import tkinter as tk

from tkinter.font import Font
from PIL import ImageTk, Image
from tifffile import imread
import ee, random, os
from resources.gee.config import EE_CREDENTIALS
from resources.gee.methods import get_ee_product
from resources.gee.vis_handler import get_visualisers_and_conf
import numpy as np
from scipy.ndimage import binary_erosion

os.chdir("..")


def get_ee_session():
    ee.Initialize(EE_CREDENTIALS)

    ee_product = get_ee_product(
        platform="sentinel",
        sensor="2",
        product="l1c"
    )
    return ee_product


class TIF_Panel(tk.Canvas):
    def __init__(self, master, width=512, height=512, bg_c="#000000"):
        tk.Canvas.__init__(self, master, width=width, height=height, background=bg_c)
        self.width = width
        self.height = height
        self.cur_tk_img = None
        self.ee_product = get_ee_session()

        self.rgb_vis, self.vis_conf_dict = get_visualisers_and_conf()
        self.vis_names = [name for (name, t) in self.vis_conf_dict.keys() if t == "vis"]

        # self.vis_func_dict = {"s2_fire":self.vis_conf_dict["s2_fire"][0],
        #                       "s2_firethresh":self.vis_conf_dict["s2_firethresh"][0],
        #                       "s2_nbr":self.vis_conf_dict["s2_nbr"][0]}

    def update_image(self, path, cur_vis_func, threshold):
        inn = imread(path)
        out = self.vis_conf_dict[(cur_vis_func, "vis")](self.ee_product, inn, {})
        im_arr_0to1 = self.vis_conf_dict[(cur_vis_func, "conf")](self.ee_product, inn, {})

        out.thumbnail((self.width, self.height))

        self.cur_tk_img = ImageTk.PhotoImage(out)
        self.imagesprite = self.create_image(self.width / 2, self.height / 2, image=self.cur_tk_img)

        self.overlay_pil = self.render_binary_mask_as_PIL(self.generate_np_bin_mask(im_arr_0to1, threshold))
        self.overlay_pil.thumbnail((self.width, self.height))
        self.overlay = ImageTk.PhotoImage(self.overlay_pil)
        self.overlaysprite = self.create_image(self.width / 2, self.height / 2, image=self.overlay)

    def render_binary_mask_as_PIL(self, binary_mask, colour_rgb=[255, 0, 255]):
        assert (len(binary_mask.shape) == 2)

        w, h = binary_mask.shape
        rgb_channels = [np.ones((w, h)) * v for v in colour_rgb]

        alpha_channel = self.highlight_borders(binary_mask * 127)
        ch4 = np.dstack((rgb_channels + [alpha_channel]))

        self.pilim = Image.fromarray(ch4.astype(np.uint8))

        return self.pilim

    def highlight_borders(self, binary_mask, border_width=5, internal_alpha=0.7):
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
        return (binary_mask * internal_alpha) + (edges * (1 - internal_alpha))

    def generate_np_bin_mask(self, im_arr_0to1, threshold):
        t = threshold / 100
        return im_arr_0to1 >= t


class Labeler(tk.Frame):
    def __init__(self, master=None, renderer_size=(256, 256)):
        self.colours = {"accent": "#005082",
                        "bg": "#000839",
                        "button": "#00a8cc",
                        "button_text": "#BBBBBB"}
        tk.Frame.__init__(self, master, bg=self.colours["accent"])
        self.master = master
        self.size = (renderer_size[0], renderer_size[1] + 64)
        self.paths = []

        self.button_font = Font(size=16, family="Symbol")

        self.base_dir = 'resources/temp-for-tool/'
        self.unlabeled_dir = self.base_dir + "unlabeled/"
        self.accepted_dir = self.base_dir + "positive/"
        self.rejected_dir = self.base_dir + "negative/"

        self.update_image_paths()
        self.cur_img_path = self.paths[0]

        self.renderer = TIF_Panel(master=self,
                                  width=renderer_size[0],
                                  height=renderer_size[1],
                                  bg_c=self.colours["bg"])

        # self.vis_renderers = [TIF_Panel(master = self,
        #                           width=renderer_size[0]//3,
        #                           height=renderer_size[1]//3,
        #                           bg_c=self.colours["bg"]),
        #                       TIF_Panel(master=self,
        #                                 width=renderer_size[0]//3,
        #                                 height=renderer_size[1]//3,
        #                                 bg_c=self.colours["bg"]),
        #                       TIF_Panel(master=self,
        #                                 width=renderer_size[0]//3,
        #                                 height=renderer_size[1]//3,
        #                                 bg_c=self.colours["bg"])]

        self.newImageButton = tk.Button(self, text="Roll", command=self.render_random_image, bg=self.colours["button"])
        self.newImageButton["font"] = self.button_font

        self.refreshButton = tk.Button(self, text="Refr.", command=self.refresh_panel_image, bg=self.colours["button"])
        self.refreshButton["font"] = self.button_font

        self.swipeRightButton = tk.Button(self, text="+ve", command=self.label_pos, bg=self.colours["button"])
        self.swipeRightButton["font"] = self.button_font

        self.swipeLeftButton = tk.Button(self, text="-ve", command=self.label_neg, bg=self.colours["button"])
        self.swipeLeftButton["font"] = self.button_font

        options = self.renderer.vis_names
        self.cur_filt_string = tk.StringVar(self)
        self.cur_filt_string.set("s2_fire")
        self.filter_chooser = tk.OptionMenu(self, self.cur_filt_string,
                                            *options)  # , command=self.refresh_panel_image_with_filt_string)#, bg=self.colours["button"])
        self.filter_chooser.config(bg=self.colours["button"])
        self.filter_chooser["menu"].config(bg=self.colours["button"])
        self.filter_chooser["font"] = self.button_font

        self.cur_threshold = tk.IntVar(self)
        self.cur_threshold.set(50)
        self.slider = tk.Scale(self, variable=self.cur_threshold, from_=100, to_=0,
                               length=renderer_size[1])  # command=self.refresh_panel_image_with_threshold)

        # self.colour_picker = tk.colorchoose.Chooser(self)

        self.newImageButton.grid(row=0, column=0, sticky=tk.W)
        self.filter_chooser.grid(row=0, column=2, sticky=tk.E)
        self.refreshButton.grid(row=0, column=3)
        self.renderer.grid(row=1, column=0, columnspan=4)
        # self.vis_renderers[0].grid(row=2, column=0)
        # self.vis_renderers[1].grid(row=2, column=1)
        # self.vis_renderers[2].grid(row=2, column=2)

        # for a0 in range(0,3):
        #     self.vis_renderers[a0].grid(row=2, column=a0)

        self.swipeRightButton.grid(row=3, column=2, columnspan=2, sticky=tk.W)
        self.swipeLeftButton.grid(row=3, column=0, columnspan=2, sticky=tk.E)
        self.slider.grid(row=1, column=4)

        self.render_random_image()

    def update_image_paths(self):
        self.paths = [self.unlabeled_dir + name for name in os.listdir(self.unlabeled_dir)]

    def refresh_panel_image_with_threshold(self, threshold: int):
        self.refresh_panel_image(threshold=threshold)

    def refresh_panel_image_with_filt_string(self, filt_string: str):
        self.refresh_panel_image(filt_string=filt_string)

    def refresh_panel_image(self, filt_string: str = None, threshold: int = None):
        cur_filt_string = self.cur_filt_string.get()
        cur_threshold = self.cur_threshold.get()
        if filt_string is not None:
            print(filt_string)
            assert (filt_string == cur_filt_string)
        if threshold is not None:
            print(threshold)
            print(cur_threshold)  #
            print()
            assert (int(threshold) == int(cur_threshold))
        self.renderer.update_image(self.cur_img_path, cur_filt_string, cur_threshold)

    def render_random_image(self):
        self.cur_img_path = random.choice(self.paths)
        self.refresh_panel_image()

    def label_pos(self):
        self.move_and_get_new(self.accepted_dir)

    def label_neg(self):
        self.move_and_get_new(self.rejected_dir)

    def move_and_get_new(self, dest_path):
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        print("Move to " + dest_path)

        print(dest_path)
        print(os.path.exists(self.cur_img_path))
        print(os.path.exists(dest_path))
        file_name = os.path.split(self.cur_img_path)[-1]
        os.rename(self.cur_img_path, dest_path + file_name)
        self.render_random_image()
        self.update_image_paths()


def b1(event):
    x, y = event.x, event.y
    print(x, y)


root = tk.Tk()
root.bind("<Button-1>", b1)

app = Labeler(root)
app.pack()


def handle_keypress(event):
    if event.char == "r":
        app.refresh_panel_image()


root.bind("<Key>", handle_keypress)
root.mainloop()
