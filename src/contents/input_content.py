from tkinter import *

from src.contents.content import Content
from src.ui.race_selector import RaceSelector


class InputContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        RaceSelector(self.frame, {
            '2022-01-01': 4,
            '2022-01-02': 5,
        })

        self.frame.pack()
