import tkinter as tk
from tkinter import OptionMenu, StringVar

from src.utils.constants import Misc, State


class Dropdown:

    def __init__(self,
                 parent_widget,
                 options,
                 callback,
                 pack_style):
        self.callback = callback
        self.options = [str(o) for o in options]
        self.selected = StringVar()
        if len(self.options) == 0:
            self.options = [Misc.NULL]

        self.selected.set(self.options[0])
        self.dropdown = OptionMenu(
            parent_widget,
            self.selected,
            *self.options,
            command=self.callback
        )
        self.dropdown.pack(pack_style)

    def set_options(self, new_options: list):
        self.options = [str(o) for o in new_options]
        if len(self.options) == 0:
            self.options = [Misc.NULL]

        self.selected.set(self.options[0])
        self.dropdown['menu'].delete(0, 'end')

        for opt in self.options:
            self.dropdown['menu'].add_command(
                label=opt, command=tk._setit(self.selected, opt, self.callback)
            )

    def get_selected_option(self):
        return self.selected.get()

    def select(self, new_option):
        if new_option in self.options:
            self.selected.set(new_option)

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

    def enable(self):
        self.dropdown.configure(state=State.NORMAL)

    def disable(self):
        self.dropdown.configure(state=State.DISABLE)
