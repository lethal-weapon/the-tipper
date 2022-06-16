from tkinter import *
from src.contents.content import Content


class InputContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        Label(self.parent, text='Input Contents').pack()
