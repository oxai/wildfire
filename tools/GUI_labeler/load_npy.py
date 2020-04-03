import numpy as np

from tools.GUI_labeler.mask_helpers import render_binary_mask_as_pil


def display_npy_file(path):
    arr = np.load(path)
    pil = render_binary_mask_as_pil(arr)
    pil.show()


if __name__ == "__main__":
    display_npy_file(input("Path?"))
