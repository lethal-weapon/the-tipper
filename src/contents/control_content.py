from threading import Thread
from datetime import datetime, timedelta
from tkinter import Frame, Label, Button, LEFT

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.storage.storage import Storage
from src.robots.race import RaceRobot
from src.robots.dividend import DividendRobot
from src.robots.manager import RobotManager
from src.utils.constants import Race, State, Time
from src.utils.general import get_now, get_current_date_and_time

RACE_DATE_OPTION_COUNT = 3


class ControlContent(Content):

    def __init__(
        self,
        parent_widget,
        recreate_contents,
        refresh_portfolio_content,
    ):
        super().__init__(parent_widget)
        self.recreate_contents = recreate_contents
        self.refresh_portfolio_content = refresh_portfolio_content

        self.info = None
        self.race_date = None

        self.btn_card = None
        self.btn_dividend = None
        self.btn_odds_start = None
        self.btn_odds_stop = None

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
            font='Times 18 italic',
        ).pack(side=LEFT, padx=30)
        self.info = Label(
            info_frame,
            text='',
            font='Times 18 bold',
        )
        self.info.pack(side=LEFT)
        info_frame.pack(pady=40)

    def build_button_frame(self):
        button_frame = Frame(self.frame)
        for i in range(1, 4):
            Label(button_frame, text=f'{i}.', font='Times 18') \
                .grid(row=i, column=1, padx=20, pady=15)
            if i == 3:
                Label(button_frame, text='Odds & Pools', font='Times 20 bold') \
                    .grid(row=i, column=2, padx=20, pady=15)

        button_options = [
            {
                'row': 1,
                'column': 2,
                'text': 'Fetch racecards',
                'command': self.on_race_card_fetched,
            },
            {
                'row': 2,
                'column': 2,
                'text': 'Fetch dividends',
                'command': self.on_dividend_fetched,
            },
            {
                'row': 3,
                'column': 3,
                'text': 'Start',
                'command': self.on_odds_started,
            },
            {
                'row': 3,
                'column': 4,
                'text': 'Stop',
                'command': self.on_odds_stopped,
            },
        ]

        for option in button_options:
            button = Button(
                button_frame,
                text=option['text'],
                font='Times 18 bold',
                width=6 if option['row'] > 2 else 15,
                borderwidth=3,
                command=option['command']
            )
            button.grid(
                row=option['row'],
                column=option['column'],
                padx=20,
                pady=15,
            )
            if option['row'] == 1:
                self.btn_card = button
            elif option['row'] == 2:
                self.btn_dividend = button
            elif 'Start' in option['text']:
                self.btn_odds_start = button
            elif 'Stop' in option['text']:
                self.btn_odds_stop = button
                self.btn_odds_stop.configure(state=State.DISABLE)

        date_wrapper = Frame(button_frame)
        self.race_date = Dropdown(
            date_wrapper,
            Storage.get_race_dates()[:RACE_DATE_OPTION_COUNT],
            lambda e: None,
            {},
        )
        date_wrapper.grid(row=2, column=3, padx=20, pady=15)
        button_frame.pack(pady=40)

    def update_info(self):
        if Storage.is_empty():
            self.info.configure(text=f'NO RACE FOUND!')
            return

        race = Storage.get_race(Storage.get_most_recent_race_date(), 1)
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
        for button in [
            self.btn_card, self.btn_dividend, self.btn_odds_start
        ]:
            button.configure(state=State.NORMAL)
        self.set_success_message('Done.')

    def disable_ui(self):
        self.race_date.disable()
        for button in [
            self.btn_card, self.btn_dividend,
            self.btn_odds_start, self.btn_odds_stop
        ]:
            button.configure(state=State.DISABLE)
        self.set_info_message('Working on it...')

    def on_race_card_fetched(self):
        self.disable_ui()
        self.worker = Thread(target=RaceRobot().run)
        self.worker.start()
        self.frame.after(250, self.check_race_card_worker)

    def check_race_card_worker(self):
        if self.worker.is_alive():
            self.frame.after(250, self.check_race_card_worker)
        else:
            self.update_info()
            self.race_date.set_options(
                Storage.get_race_dates()[:RACE_DATE_OPTION_COUNT])
            self.enable_ui()
            self.recreate_contents()

    def on_dividend_fetched(self):
        selected_date = self.race_date.get_selected_option()
        first_race_time = \
            datetime.fromisoformat(Storage.get_race(selected_date, 1)[Race.TIME])

        if get_now() <= first_race_time:
            self.set_info_message(f'Meeting {selected_date} has not yet started.')
            return

        self.disable_ui()
        self.worker = Thread(
            target=DividendRobot().run,
            kwargs={Race.RACE_DATE: selected_date}
        )
        self.worker.start()
        self.frame.after(250, self.check_dividend_worker)

    def check_dividend_worker(self):
        if self.worker.is_alive():
            self.frame.after(250, self.check_dividend_worker)
        else:
            self.enable_ui()

    def on_odds_started(self):
        race_date = Storage.get_most_recent_race_date()
        if not RobotManager.can_work_on(race_date):
            self.set_info_message(
                f'Can not work on the meeting {race_date} right now.')
            return

        self.disable_ui()
        self.worker = Thread(
            name=f'Thread <{race_date}>',
            target=RobotManager.work,
            kwargs={'race_date_to_work': race_date}
        )
        self.worker.start()
        self.frame.after(1000, self.check_odds_worker_started)

    def check_odds_worker_started(self):
        if self.worker.is_alive():
            self.btn_odds_stop.configure(state=State.NORMAL)
            self.refresh_portfolio_until_odds_stopped()
        else:
            self.frame.after(1000, self.check_odds_worker_started)

    def on_odds_stopped(self):
        self.disable_ui()

        if self.worker.is_alive():
            RobotManager.stop()
            self.frame.after(250, self.on_odds_stopped)
        else:
            self.enable_ui()
            self.btn_odds_stop.configure(state=State.DISABLE)

    def refresh_portfolio_until_odds_stopped(self):
        self.refresh_portfolio_content()

        if self.worker.is_alive():
            self.frame.after(
                Time.REFRESH_FREQUENCY_MS,
                self.refresh_portfolio_until_odds_stopped
            )
