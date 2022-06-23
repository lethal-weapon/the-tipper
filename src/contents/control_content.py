from tkinter import Frame, Label, Button, LEFT
from datetime import datetime, timedelta

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.storage.storage import Storage
from src.utils.constants import Race
from src.utils.general import get_current_date_and_time


class ControlContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.info = None
        self.race_date = None
        self.build_info_frame()
        self.build_button_frame()
        self.pack_message()
        self.frame.pack()
        self.update_info()

    def build_info_frame(self):
        info_frame = Frame(self.frame)
        Label(
            info_frame,
            text='Next Meeting:',
            font='Times 16 italic',
        ).pack(side=LEFT, padx=30)
        self.info = Label(
            info_frame,
            text='',
            font='Times 16 bold',
        )
        self.info.pack(side=LEFT)
        info_frame.pack(pady=20)

    def build_button_frame(self):
        outer_frame = Frame(self.frame)
        label_frame = Frame(outer_frame)
        Label(label_frame, text='Fetch/Update', font='Times 18').pack()
        label_frame.pack()

        button_frame = Frame(outer_frame)
        button_options = [
            {
                'row': 1,
                'column': 1,
                'text': 'race cards',
                'command': self.on_race_card_pressed,
            },
            {
                'row': 2,
                'column': 1,
                'text': 'race result',
                'command': self.on_race_result_pressed,
            },
            {
                'row': 2,
                'column': 2,
                'text': 'odds & pools',
                'command': self.on_odds_pool_pressed,
            },
        ]

        for option in button_options:
            Button(button_frame,
                   text=option['text'],
                   font='Times 18 bold',
                   width=13,
                   borderwidth=3,
                   command=option['command']) \
                .grid(row=option['row'],
                      column=option['column'],
                      padx=30,
                      pady=10)

        date_wrapper = Frame(button_frame)
        self.race_date = Dropdown(
            date_wrapper,
            Storage.get_race_dates(),
            lambda e: None,
            {},
        )
        date_wrapper.grid(row=1, column=2, padx=30, pady=10)
        button_frame.pack(pady=20)
        outer_frame.pack(pady=50)

    def update_info(self):
        error_msg = 'Unknown (fetch race cards below)'
        if Storage.is_empty():
            self.info.configure(text=error_msg)
            return

        race = Storage.get_race(Storage.get_race_dates()[0], 1)
        race_time = datetime.fromisoformat(race[Race.TIME])
        race_venue = race[Race.VENUE]

        curr_date, curr_time = get_current_date_and_time()
        race_date, race_time = datetime.date(race_time), datetime.time(race_time)

        if race_date < curr_date:
            self.info.configure(text=error_msg)
            return

        if race_date == curr_date:
            date_part = 'Today'
        elif race_date - curr_date == timedelta(days=1):
            date_part = 'Tomorrow'
        else:
            date_part = f'{race_date.strftime("%A")[:3]}  {race_date}'

        if race_time.hour > 12:
            time_part = f'{race_time.hour % 12}:{race_time.minute}'
        else:
            time_part = f'{race_time.hour}:{race_time.minute}'

        self.info.configure(text=f'{race_venue}, {date_part}  @{time_part} pm')

    def on_race_card_pressed(self):
        pass

    def on_race_result_pressed(self):
        pass

    def on_odds_pool_pressed(self):
        pass
