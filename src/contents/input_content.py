from tkinter import Button

from src.storage.storage import Storage
from src.utils.constants import Tip, MessageLevel
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
            Storage.get_race_date_and_num_count(),
            50
        )
        self.tipster_picker = TipsterSelector(
            self.frame,
            self.load,
            30
        )
        self.horse_entry = HorseEntry(
            self.frame,
            4,
            30
        )
        Button(
            self.frame,
            text='Save',
            font='Times 18 bold',
            width=10,
            borderwidth=5,
            command=self.save
        ).pack(pady=40)

        self.pack_message()
        self.frame.pack()
        self.load()

    def load(self):
        """ Loads tips from storage according to the UI state. """
        if Storage.is_empty():
            self.set_message(MessageLevel.INFO, 'No race found.')
            return

        race_date, race_num = \
            self.race_picker.get_race_date_num()
        source, tipster, is_confident = \
            self.tipster_picker.get_source_tipster_confident()
        prefix = f'{tipster} tips'
        msg_loaded, msg_non_exist, msg_fail = \
            f'{prefix} loaded.', \
            f'{prefix} does not exist.', \
            f'{prefix} failed to load.'

        # reset the entry fields before loading anything
        self.tipster_picker.set_confident(False)
        self.horse_entry.clear()

        try:
            tip = Storage.get_tip(race_date, race_num, source, tipster)
            if tip is None:
                self.set_message(MessageLevel.INFO, msg_non_exist)
                return

            self.tipster_picker.set_confident(tip[Tip.CONFIDENT])
            self.horse_entry.set_values(tip[Tip.TIP])
            self.set_message(MessageLevel.SUCCESS, msg_loaded)
        except RuntimeError as ex:
            self.set_message(MessageLevel.ERROR, str(ex))
        except:
            self.set_message(MessageLevel.ERROR, msg_fail)

    def save(self):
        """ Save tips into storage according to the UI state. """
        if Storage.is_empty():
            self.set_message(MessageLevel.ERROR, 'No race found.')
            return

        race_date, race_num = \
            self.race_picker.get_race_date_num()
        source, tipster, is_confident = \
            self.tipster_picker.get_source_tipster_confident()
        tip = self.horse_entry.get_values()
        prefix = f'{tipster} tips'
        msg_saved, msg_fail = \
            f'{prefix} saved.', \
            f'{prefix} failed to save.'

        try:
            Storage.save_tip(race_date, race_num, {
                Tip.SOURCE: source,
                Tip.TIPSTER: tipster,
                Tip.TIP: tip,
                Tip.CONFIDENT: is_confident,
            })
            self.set_message(MessageLevel.SUCCESS, msg_saved)
        except:
            self.set_message(MessageLevel.ERROR, msg_fail)
