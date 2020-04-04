# Launch tkinter application for labeling/generating masks for tiff images

from tools.GUI_labeler.Window import Window
import tkinter as tk
import argparse

parser = argparse.ArgumentParser(description="Image and metric visualiser")
parser.add_argument("unlabeled_image_directory")
parser.add_argument("--inplace", "-i", action='store_true')
parser.add_argument("--move_to", "-m", required=False, help="directory to which images should be moved")
parser.add_argument("--copy_to", "-c", required=False, help="directory to which images should be copied")
args = parser.parse_args()

# Make sure only one save option has been specified
if sum([args.inplace, args.move_to is not None, args.copy_to is not None]) != 1:
    raise Exception("You must choose exactly one of inplace, move_to and copy_to")

unlabeled_dir = args.unlabeled_image_directory

if args.inplace:
    move_or_copy = "move"
    labeled_dir = unlabeled_dir
elif args.move_to is not None:
    labeled_dir = args.move_to
    move_or_copy = "move"
elif args.copy_to is not None:
    labeled_dir = args.copy_to
    move_or_copy = "copy"
else:
    raise Exception("This should not occur!")

root = tk.Tk()
app = Window(master=None,
             unlabeled_dir=unlabeled_dir,
             labeled_dir=labeled_dir,
             move_or_copy=move_or_copy)


def b1(event):
    if event.char == "r":
        app.update_main_masks()


root.bind("<Key>", b1)

root.iconphoto(False, tk.PhotoImage(file='tools/GUI_labeler/icon.png'))

app.pack()
root.mainloop()
