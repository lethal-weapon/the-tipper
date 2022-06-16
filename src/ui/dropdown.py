from tkinter import *

from src.utils.constants import Misc


class Dropdown:

    def __init__(self, parent_widget, options, callback, pack_style):
        self.options = [str(o) for o in options]
        self.selected = StringVar()
        self.selected.set(Misc.NULL)
        if len(options) > 0:
            self.selected.set(options[0])

        self.dropdown = OptionMenu(
            parent_widget,
            self.selected,
            *options,
            command=callback
        )
        self.dropdown.pack(pack_style)

    def get_selected_option(self):
        return self.selected.get()

    def select_first(self):
        self.selected.set(self.options[0])

    def select_last(self):
        self.selected.set(self.options[len(self.options) - 1])

    def select_previous(self):
        curr = self.options.index(self.get_selected_option())
        if 1 <= curr <= len(self.options) - 1:
            self.selected.set(self.options[curr - 1])

    def select_next(self):
        curr = self.options.index(self.get_selected_option())
        if 0 <= curr < len(self.options) - 1:
            self.selected.set(self.options[curr + 1])

    def is_first(self):
        curr = self.options.index(self.get_selected_option())
        return curr == 0

    def is_last(self):
        curr = self.options.index(self.get_selected_option())
        return curr == len(self.options) - 1
