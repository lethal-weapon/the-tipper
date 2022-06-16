from tkinter import *
from src.contents.content import Content


class PerformanceContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        Label(self.parent, text='Performance Contents').pack()
