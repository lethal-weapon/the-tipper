from threading import Thread
from tkinter import Frame, Label, Button, LEFT
from datetime import datetime, timedelta

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.storage.storage import Storage
from src.utils.constants import Race, State, MessageLevel
from src.utils.general import get_current_date_and_time
from src.robots.race_robot import RaceRobot


class ControlContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.info = None
        self.race_date = None

        self.btn_card = None
        self.btn_odds = None
        self.btn_result = None

        self.worker = None

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
            button = Button(
                button_frame,
                text=option['text'],
                font='Times 18 bold',
                width=13,
                borderwidth=3,
                command=option['command']
            )
            button.grid(
                row=option['row'],
                column=option['column'],
                padx=30,
                pady=10,
            )
            if 'card' in option['text']:
                self.btn_card = button
            elif 'result' in option['text']:
                self.btn_result = button
            elif 'odds' in option['text']:
                self.btn_odds = button

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
        if Storage.is_empty():
            self.info.configure(text=f'NO RACE FOUND!')
            return

        race = Storage.get_race(Storage.get_race_dates()[0], 1)
        race_time = datetime.fromisoformat(race[Race.TIME])
        race_venue = race[Race.VENUE]

        curr_date, curr_time = get_current_date_and_time()
        race_date, race_time = datetime.date(race_time), datetime.time(race_time)

        if race_date < curr_date:
            self.info.configure(text='Unknown (fetch race cards below)')
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

        if time_part.endswith(':0'):
            time_part += '0'

        self.info.configure(text=f'{race_venue}, {date_part}  @{time_part} pm')

    def enable_ui(self):
        self.race_date.enable()
        for button in [self.btn_card, self.btn_result, self.btn_odds]:
            button.configure(state=State.NORMAL)

    def disable_ui(self):
        self.race_date.disable()
        for button in [self.btn_card, self.btn_result, self.btn_odds]:
            button.configure(state=State.DISABLE)

    def on_race_card_pressed(self):
        self.disable_ui()
        self.set_message(MessageLevel.INFO, 'Working on it...')

        bot = RaceRobot()
        self.worker = Thread(target=bot.run)
        self.worker.start()
        self.frame.after(250, self.check_race_card_worker)

    def on_race_result_pressed(self):
        self.disable_ui()
        self.set_message(MessageLevel.INFO, 'Working on it...')

    def on_odds_pool_pressed(self):
        self.disable_ui()
        self.set_message(MessageLevel.INFO, 'Working on it...')

    def check_race_card_worker(self):
        if self.worker.is_alive():
            self.frame.after(250, self.check_race_card_worker)
        else:
            self.update_info()
            self.race_date.set_options(Storage.get_race_dates())
            self.enable_ui()
            self.set_message(MessageLevel.SUCCESS, 'Done.')
