from tkinter import *

from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.ui.tipster_selector import TipsterSelector
from src.ui.horse_entry import HorseEntry


class InputContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.race_picker = RaceSelector(self.frame, {
            '2022-01-01': 4,
            '2022-01-02': 5,
        }, 30)
        self.tipster_picker = TipsterSelector(self.frame, 20)
        self.horse_entry = HorseEntry(self.frame, 4, 40)
        Button(self.frame,
               text='Save',
               font='Times 18 bold',
               width=10,
               borderwidth=5,
               command=self.save) \
            .pack(pady=30)

        self.frame.pack()

    def save(self):
        print(f'{self.race_picker.get_race_date_num()}\n'
              f'{self.tipster_picker.get_source_tipster_confident()}\n'
              f'{self.horse_entry.get_values()}')
