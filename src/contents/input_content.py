from tkinter import *

from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.ui.tipster_selector import TipsterSelector
from src.ui.horse_entry import HorseEntry


class InputContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.race_picker = RaceSelector(
            self.frame,
            self.load,
            self.get_race_days(),
            30
        )
        self.tipster_picker = TipsterSelector(
            self.frame,
            self.load,
            20
        )
        self.horse_entry = HorseEntry(
            self.frame,
            4,
            40
        )
        Button(self.frame,
               text='Save',
               font='Times 18 bold',
               width=10,
               borderwidth=5,
               command=self.save) \
            .pack(pady=30)

        self.pack_message()
        self.frame.pack()

    def save(self):
        """ Save tips into storage according to the UI state. """
        race_date, race_num = \
            self.race_picker.get_race_date_num()
        source, tipster, is_confident = \
            self.tipster_picker.get_source_tipster_confident()
        tips = \
            self.horse_entry.get_values()

        try:
            # TODO: saving
            self.set_message(True, f'{tipster} tips saved.')
        except:
            self.set_message(False, f'{tipster} tips failed to save.')

    def load(self):
        """ Loads tips from storage according to the UI state. """
        race_date, race_num = \
            self.race_picker.get_race_date_num()
        source, tipster, is_confident = \
            self.tipster_picker.get_source_tipster_confident()

        try:
            # TODO: loading
            print(f'Loading tips for '
                  f'<{race_date}, {race_num}, {source}, {tipster}>')
            self.set_message(True, f'{tipster} tips loaded.')
        except:
            self.set_message(False, f'{tipster} tips failed to load.')

    @staticmethod
    def get_race_days() -> dict:
        """
        Return up to the most recent 5 race days
        and the total races for each one of them.
        """
        return {
            '2022-01-01': 4,
            '2022-01-02': 5,
        }
