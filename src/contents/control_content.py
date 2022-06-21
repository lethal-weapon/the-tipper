from tkinter import *
from datetime import datetime, timedelta

from src.contents.content import Content
from src.storage.storage import Storage
from src.utils.constants import Race, MessageLevel
from src.utils.general import get_current_date_and_time


class ControlContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

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
        info_frame.pack(pady=30)

        self.pack_message()
        self.frame.pack()
        self.update_info()

    def update_info(self):
        race = Storage.get_race(Storage.get_race_dates()[0], 1)
        race_time = datetime.fromisoformat(race[Race.TIME])
        race_venue = race[Race.VENUE]

        curr_date, curr_time = get_current_date_and_time()
        race_date, race_time = datetime.date(race_time), datetime.time(race_time)

        if race_date < curr_date:
            self.info.configure(text=f'Unknown (fetch it below)')
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
