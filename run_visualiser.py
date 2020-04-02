# Launch tkinter application for labeling/generating masks for tiff images

from resources.GUI_labeler.Window import Window
import tkinter as tk

root = tk.Tk()
app = Window()


def b1(event):
    if event.char == "r":
        app.update_main_masks()


root.bind("<Key>", b1)

root.iconphoto(False, tk.PhotoImage(file='resources/GUI_labeler/icon.png'))

app.pack()
root.mainloop()
