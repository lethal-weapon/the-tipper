from tkinter import Label

from src.storage.storage import Storage
from src.contents.content import Content
from src.ui.race_selector import RaceSelector


class PortfolioContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.race_picker = RaceSelector(
            self.frame,
            self.load,
            Storage.get_race_date_and_num_count(),
            30
        )

        self.pack_message()
        self.frame.pack()
        self.load()

    def load(self):
        """ Update tips/portfolios according to the race date/num. """

        race_date, race_num = \
            self.race_picker.get_race_date_num()
