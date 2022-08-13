from tkinter import Frame, Label, Radiobutton, StringVar, LEFT

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.storage.cache import Cache
from src.utils.constants import Color, IGNORED_PEOPLE
from src.utils.converters import to_people_name

PAGE_OPTIONS = {
    'Tipster': [
        'Last day',
        'Recent 3 days',
        'Recent 5 days',
        'Recent 10 days',
        'All times',
    ],
    'Jockey': [
        'Meeting',
        'Earning 21/22',
        'Earning 22/23',
    ],
}

HEADER_FONT = 'Times 14 bold'
BODY_FONT = 'Times 12'


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
        self.content_frame.pack(pady=10)

    def build_content_frame(self):
        option_key, option_value = \
            self.option_key.get(), self.option_list.get_selected_option()

        if option_key == 'Jockey':
            if 'Earning' in option_value:
                self.build_jockey_earning_content(option_value)
            elif 'Meeting' in option_value:
                self.build_jockey_performance_content()
        else:
            Label(
                self.content_frame,
                text=f'{option_key} / {option_value}',
                font='Times 14',
            ).pack()

    def build_jockey_earning_content(self, option_value: str):
        season = option_value.split(' ')[1]
        earnings = Cache.get_jockey_earnings_by_season(season)
        headers = []

        if len(earnings) > 0:
            headers = [k for k in earnings[0].keys()]

        for header in headers:
            formatted_header = header[0].upper() + header[1:]
            Label(self.content_frame, text=formatted_header, font=HEADER_FONT) \
                .grid(row=1, column=1 + headers.index(header), padx=6, pady=2)

        row = 1
        for earning in earnings:
            row += 1
            for header in headers:
                value = str(earning[header])
                if 'jockey' in header:
                    if value in IGNORED_PEOPLE:
                        break
                    value = to_people_name(value)

                Label(self.content_frame, text=value, font=BODY_FONT,
                      fg=self.get_earning_color(header.lower(), value)) \
                    .grid(row=row, column=1 + headers.index(header), padx=6)

    @staticmethod
    def get_earning_color(field: str, value: str) -> str:
        if 'rich' in field and float(value) >= 0.4:
            return Color.ORANGE

        elif 'earndayavg' in field and float(value) >= 12:
            return Color.RED

        return Color.BLACK

    def build_jockey_performance_content(self):
        performance = Cache.get_jockey_performance_by_meeting()
