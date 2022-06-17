from tkinter import *

from src.ui.dropdown import Dropdown


class RaceSelector:

    def __init__(self, parent_widget, races: dict):
        frame = Frame(parent_widget)
        self.races = races

        font_style = 'Times 16 italic'
        regular_style = {'side': LEFT, 'padx': 10, 'pady': 30}
        button_style = {'side': RIGHT, 'padx': 5, 'pady': 30}

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
        Button(frame, text='Previous', command=self.to_previous).pack(button_style)
        Button(frame, text='Next', command=self.to_next).pack(button_style)

        frame.pack()

    def get_race_date_num(self) -> (str, str):
        return self.race_date.get_selected_option(), \
               self.race_num.get_selected_option()

    def get_race_dates(self) -> [str]:
        dates = list(self.races.keys())
        dates.sort(reverse=True)
        return dates

    def get_race_nums(self) -> [str]:
        races = self.races[self.race_date.get_selected_option()]
        return [str(r) for r in range(1, races + 1)]

    def on_race_changed(self):
        print(self.get_race_date_num())

    def on_date_changed(self, e):
        # save the current race num
        curr_num = self.race_num.get_selected_option()

        # load the new race nums for this race day
        self.race_num.set_options(self.get_race_nums())

        # keep the race num if exists, use the max num if not
        self.race_num.select_last()
        if curr_num in self.get_race_nums():
            self.race_num.select(curr_num)

        self.on_race_changed()

    def on_num_changed(self, e):
        self.on_race_changed()

    def to_previous(self):
        if self.race_num.is_first():
            if self.race_date.is_last():
                return

            self.race_date.select_next()
            self.race_num.set_options(self.get_race_nums())
            self.race_num.select_last()
        else:
            self.race_num.select_previous()

        self.on_race_changed()

    def to_next(self):
        if self.race_num.is_last():
            if self.race_date.is_first():
                return

            self.race_date.select_previous()
            self.race_num.set_options(self.get_race_nums())
            self.race_num.select_first()
        else:
            self.race_num.select_next()

        self.on_race_changed()
