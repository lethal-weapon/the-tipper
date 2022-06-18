from tkinter import *

from src.utils.constants import Style, Color


class Content:

    def __init__(self, parent_widget):
        self.frame = Frame(parent_widget)
        self.message = Label(self.frame, text='', font='Times 12')

    def pack_message(self):
        self.message.pack(side=RIGHT)

    def set_message(self, is_success: bool, text: str):
        self.message.__setitem__(Style.TEXT, text)

        if is_success:
            self.message.__setitem__(Style.FG, Color.GREEN)
        else:
            self.message.__setitem__(Style.FG, Color.RED)
