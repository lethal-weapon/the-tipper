import json
from tkinter import Frame, Label, Radiobutton, StringVar, LEFT

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.utils.constants import Color, QueryFile
from src.utils.database import Database
from src.utils.cypher_converter import CypherConverter

PAGE_OPTIONS = {
    'Tipster': [
        'Last day',
        'Recent 3 days',
        'Recent 5 days',
        'Recent 10 days',
        'All times',
    ],
    'Jockey': [
        'Earning 21/22',
        'Earning 22/23',
        'Meeting',
    ],
}

SEASON_DATES = {
    '21/22': ('2021-09-05', '2022-07-16'),
    '22/23': ('2022-09-11', '2023-07-16'),
}


class PerformanceContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.header_frame = Frame(self.frame)
        self.option_key = StringVar()
        self.option_list = None
        self.build_header_frame()
        self.header_frame.pack()

        self.content_frame = None
        self.update_content_frame()
        self.frame.pack()

    def build_header_frame(self):
        for k in PAGE_OPTIONS.keys():
            Radiobutton(
                self.header_frame,
                text=k,
                value=k,
                variable=self.option_key,
                command=self.update_option_list,
                font='Times 16 bold',
            ).pack(padx=15, side=LEFT)

        self.option_key.set('Jockey')

        Label(
            self.header_frame,
            text='By',
            font='Times 16 italic',
            fg=Color.BLUE,
        ).pack(padx=20, side=LEFT)

        self.option_list = Dropdown(
            self.header_frame,
            PAGE_OPTIONS[self.option_key.get()],
            self.update_content_frame,
            {'side': LEFT, 'padx': 15},
        )

    def update_option_list(self, *e):
        self.option_list.set_options(
            PAGE_OPTIONS[self.option_key.get()]
        )
        self.update_content_frame()

    def update_content_frame(self, *e):
        if self.content_frame:
            self.content_frame.pack_forget()
            self.content_frame.destroy()

        self.content_frame = Frame(self.frame)
        self.build_content_frame()
        self.content_frame.pack(pady=15)

    def build_content_frame(self):
        option_key, option_value = \
            self.option_key.get(), self.option_list.get_selected_option()

        if option_key == 'Jockey' and 'Earning' in option_value:
            self.build_jockey_earning_content(option_value)
        else:
            Label(
                self.content_frame,
                text=f'{option_key} / {option_value}',
                font='Times 14',
            ).pack()

    def build_jockey_earning_content(self, option_value: str):
        season = SEASON_DATES[option_value.split(' ')[1]]
        params = {
            '$startDate': CypherConverter.to_date(season[0]),
            '$endDate': CypherConverter.to_date(season[1]),
        }
        records = Database.read_from_file(
            QueryFile.JOCKEY_EARNING,
            params
        )
        for record in records:
            record_data = record.data()
            print(json.dumps(record_data, sort_keys=False, indent=4))

        # {
        #     "jockey": "Zac Purton",
        #     "rideDays": 79,
        #     "earnDays": 79,
        #     "totalEarns": 933.3,
        #     "earnDayAvg": 11.8,
        #     "rideDayAvg": 11.8,
        #     "realAvg": 11.8,
        #     "poor": 0.22,
        #     "regular": 0.39,
        #     "rich": 0.39
        # }
