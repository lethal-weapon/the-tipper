from tkinter import *

from src.contents.content import Content


class PortfolioContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        Label(self.frame, text='Portfolio Contents').pack()

        self.frame.pack()
