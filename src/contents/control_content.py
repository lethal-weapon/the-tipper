from tkinter import *

from src.contents.content import Content


class ControlContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        Label(self.frame, text='Control Contents').pack()

        self.frame.pack()
