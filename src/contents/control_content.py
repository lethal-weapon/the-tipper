from tkinter import *
from src.contents.content import Content
from src.ui.dropdown import Dropdown


class ControlContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        frame = Frame(self.parent)

        regular_style = {'side': LEFT, 'padx': 10, 'pady': 10}
        button_style = {'side': RIGHT, 'padx': 3, 'pady': 10}

        Label(frame, text='Meeting', font='Times 16 italic').pack(regular_style)
        self.race_date = Dropdown(
            frame, self.get_dates(), self.on_race_changed, regular_style
        )

        Label(frame, text='').pack(regular_style)
        Label(frame, text='Race #', font='Times 16 italic').pack(regular_style)
        self.race_num = Dropdown(
            frame, self.get_numbers(), self.on_race_changed, regular_style
        )

        Label(frame, text='').pack(regular_style)
        Button(frame, text='Previous', command=self.to_previous).pack(button_style)
        Button(frame, text='Next', command=self.to_next).pack(button_style)

        frame.pack()

    def on_race_changed(self, e):
        print(f'{self.race_date.get_selected_option()}, '
              f'{self.race_num.get_selected_option()}')

    @staticmethod
    def get_dates():
        return [
            '2022-01-02',
            '2022-01-01',
        ]

    @staticmethod
    def get_numbers():
        return [i for i in range(1, 5)]

    def to_previous(self):
        if self.race_num.is_first():
            if self.race_date.is_last():
                return

            self.race_date.select_next()
            self.race_num.select_last()
        else:
            self.race_num.select_previous()

        self.on_race_changed(0)

    def to_next(self):
        if self.race_num.is_last():
            if self.race_date.is_first():
                return

            self.race_date.select_previous()
            self.race_num.select_first()
        else:
            self.race_num.select_next()

        self.on_race_changed(0)
