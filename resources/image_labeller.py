from tkinter import *

import os
from PIL import Image, ImageTk
import random


class TifDisplayer(Frame):
    def __init__(self, master=None, render_dims=(312,443)):
        Frame.__init__(self, master)
        self.master = master

        self.render_dims=render_dims
        self.window_size = (render_dims[0], render_dims[1] + 64)

        self.update_image_paths()

        self.pack(fill=BOTH, expand=1)

        self.newImageButton = Button(self, text="Roll", command=self.render_random_image)
        self.newImageButton.place(x=0, y=512)
        self.render_random_image()


    def render_random_image(self):
        print("Rendering new image")
        self.render_new_image(random.choice(self.paths))

    def render_new_image(self, path):
        load = Image.open(path)
        load = load.resize((512,512))
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        return img.size()


    def update_image_paths(self):
        subdir_path = 'gee/data_dir/temp-for-tool/unlabelled/'
        self.paths = [subdir_path + name for name in os.listdir(subdir_path)]


root = Tk()
app = TifDisplayer(root)
root.wm_title("Tkinter window")
root.geometry("{w}x{h}".format(w=app.window_size[0], h=app.window_size[1]))
root.mainloop()