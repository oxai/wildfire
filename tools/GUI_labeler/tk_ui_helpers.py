import tkinter as tk
from typing import Callable

from tools.GUI_labeler.config import colours


def make_option_menu(master,
                     variable: tk.Variable,
                     choices: list,
                     command: Callable = None) -> tk.OptionMenu:
    """
    Creates an instance of tkinter ObjectMenu following the theme of the UI toolbar

    :param master: the tk object in which the menu should be rendered
    :param variable: the tk.Variable that should be changed by the menu
    :param choices: the choices that can be picked from the menu
    :param command: the function that should be run when an option is selected
    :return: an instance of tk.ObjectMenu
    """
    combi_chooser = tk.OptionMenu(master,
                                  variable,
                                  *choices,
                                  command=command)
    combi_chooser["fg"] = colours["toolbar_txt"]
    combi_chooser['menu'].config(bg=colours["toolbar_bg"], fg=colours["toolbar_txt"])
    combi_chooser.config(bg=colours["toolbar_bg"], bd=1)
    combi_chooser["highlightthickness"] = 0
    return combi_chooser


def make_toolbar_label(master,
                       txt: str) -> tk.Label:
    """
    Creates a label/text ui element following the theme of the UI toolbar

    :param master: the tk object in which the menu should be rendered
    :param txt: the text to be displayed
    :return: an instance of tk.Label
    """
    return tk.Label(master,
                    text=txt,
                    bg=colours["toolbar_bg"],
                    fg=colours["toolbar_txt"])


def make_toolbar_button(master,
                        txt: str,
                        command: Callable) -> tk.Button:
    """
    Creates an instance of tkinter.Button following the theme of the UI toolbar

    :param master: the tk object in which the menu should be rendered
    :param txt: the text to be rendered on the button
    :param command: the function that should be run when the button is pressed
    :return: an instance of tk.Button
    """
    return tk.Button(master, text=txt,
                     command=command,
                     bg=colours["toolbar_bg"],
                     fg=colours["toolbar_txt"],
                     bd=0)


def make_menu_bar_button(master,
                         txt: str,
                         command: Callable) -> tk.Button:
    """
    Creates an instance of tkinter.Button following the theme of the UI top-level menu_bar

    :param master: the tk object in which the menu should be rendered
    :param txt: the text to be rendered on the button
    :param command: the function that should be run when the button is pressed
    :return: an instance of tk.Button
    """
    return tk.Button(master, text=txt,
                     command=command,
                     bg=colours["menu_bar_bg"],
                     fg=colours["menu_bar_txt"],
                     bd=0)
