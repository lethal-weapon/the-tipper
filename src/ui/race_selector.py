from tkinter import Frame, Label, Button, LEFT, RIGHT

from src.ui.dropdown import Dropdown
from src.utils.constants import Misc


class RaceSelector:

    def __init__(self,
                 parent_widget,
                 callback,
                 races: dict,
                 pady: int):
        frame = Frame(parent_widget)
        self.callback = callback
        self.races = races

        font_style = 'Times 16 italic'
        regular_style = {'side': LEFT, 'padx': 10}
        button_style = {'side': RIGHT, 'padx': 5}

        Label(frame, text='Meeting', font=font_style).pack(regular_style)
        self.race_date = Dropdown(
            frame, self.get_race_dates(), self.on_date_changed, regular_style
        )

        Label(frame, text='').pack(regular_style)
        Label(frame, text='Race #', font=font_style).pack(regular_style)
        self.race_num = Dropdown(
            frame, self.get_race_nums(), self.on_num_changed, regular_style
        )

        Label(frame, text='').pack(regular_style)
        Button(frame, text='Next', command=self.to_next).pack(button_style)
        Button(frame, text='Previous', command=self.to_previous).pack(button_style)

        frame.pack(pady=pady)

    def get_race_date_num(self) -> (str, int):
        return self.race_date.get_selected_option(), \
               int(self.race_num.get_selected_option())

    def get_race_dates(self) -> [str]:
        dates = list(self.races.keys())
        dates.sort(reverse=True)
        return dates

    def get_race_nums(self) -> [str]:
        selected = self.race_date.get_selected_option()
        if selected == Misc.NULL:
            return []

        races = self.races[selected]
        return [str(r) for r in range(1, races + 1)]

    def on_changed(self, *e):
        self.callback()

    def on_date_changed(self, e):
        # save the current race num
        curr_num = self.race_num.get_selected_option()

        # load the new race nums for this race day
        self.race_num.set_options(self.get_race_nums())

        # keep the race num if exists, use the max num if not
        self.race_num.select_last()
        if curr_num in self.get_race_nums():
            self.race_num.select(curr_num)

        self.on_changed(e)

    def on_num_changed(self, e):
        self.on_changed(e)

    def to_previous(self):
        if self.race_num.is_first():
            if self.race_date.is_last():
                return

            self.race_date.select_next()
            self.race_num.set_options(self.get_race_nums())
            self.race_num.select_last()
        else:
            self.race_num.select_previous()

        self.on_changed()

    def to_next(self):
        if self.race_num.is_last():
            if self.race_date.is_first():
                return

            self.race_date.select_previous()
            self.race_num.set_options(self.get_race_nums())
            self.race_num.select_first()
        else:
            self.race_num.select_next()

        self.on_changed()
