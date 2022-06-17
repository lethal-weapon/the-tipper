from tkinter import *

from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.ui.tipster_selector import TipsterSelector


class InputContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.race_picker = RaceSelector(self.frame, {
            '2022-01-01': 4,
            '2022-01-02': 5,
        })
        self.tipster_picker = TipsterSelector(self.frame)

        self.frame.pack()
