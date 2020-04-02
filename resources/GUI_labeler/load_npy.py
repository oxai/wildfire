from resources.GUI_labeler.PIL_helpers import render_binary_mask_as_PIL
import numpy as np


def display_npy_file(path):
    arr = np.load(path)
    print(arr)
    pil = render_binary_mask_as_PIL(arr)
    pil.show()


if __name__ == "__main__":
    display_npy_file(input("Path?"))
