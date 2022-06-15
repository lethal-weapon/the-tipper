from tkinter import *
from src.ui.content import Content
from src.utils.constants import Style


class PerformanceContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        Label(self.parent, text='Performance Contents').pack()
