from tkinter import *

from src.ui.dropdown import Dropdown
from src.utils.tipster_sources import TIPSTER_SOURCES


class TipsterSelector:

    def __init__(self,
                 parent_widget,
                 callback,
                 pady: int):
        frame = Frame(parent_widget)
        self.callback = callback

        font_style = 'Times 16 italic'
        regular_style = {'side': LEFT, 'padx': 10}

        Label(frame, text='Source', font=font_style).pack(regular_style)
        self.source = Dropdown(
            frame,
            list(TIPSTER_SOURCES.keys()),
            self.on_source_changed,
            regular_style
        )

        Label(frame, text='').pack(regular_style)
        Label(frame, text='Tipster', font=font_style).pack(regular_style)
        self.tipster = Dropdown(
            frame,
            self.get_tipsters(),
            self.on_changed,
            regular_style
        )

        Label(frame, text='').pack(regular_style)
        Label(frame, text='Confident', font=font_style).pack(regular_style)
        self.confident = IntVar()
        self.confident_check = Checkbutton(
            frame,
            variable=self.confident,
        )
        self.confident_check.pack(regular_style)

        frame.pack(pady=pady)

    def get_tipsters(self) -> [str]:
        return TIPSTER_SOURCES[self.source.get_selected_option()]

    def get_source_tipster_confident(self) -> (str, str, bool):
        return self.source.get_selected_option(), \
               self.tipster.get_selected_option(), \
               self.confident.get() == 1

    def on_changed(self, *e):
        self.callback()

    def on_source_changed(self, e):
        self.tipster.set_options(TIPSTER_SOURCES[e])
        self.on_changed(e)

    def set_confident(self, is_confident: bool):
        self.confident.set(1 if is_confident else 0)
