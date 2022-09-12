from operator import itemgetter
from tkinter import Frame, Label, Radiobutton, Button, StringVar, LEFT

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.storage.cache import Cache
from src.utils.constants import \
    Color, State, IGNORED_PEOPLE, JOCKEY_RANKINGS, TRAINER_RANKINGS

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
    'Trainer': [
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
        self.active_meeting_slice = 0
        self.btn_next = None
        self.btn_prior = None
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

        self.option_key.set('Tipster')

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
        self.btn_next = Button(
            self.header_frame, text='Next', command=self.to_next_meeting)
        self.btn_prior = Button(
            self.header_frame, text='Prior', command=self.to_prior_meeting)
        self.btn_next.pack(padx=15, side=LEFT)
        self.btn_prior.pack(padx=15, side=LEFT)

    def to_next_meeting(self, *e):
        if self.active_meeting_slice > 0:
            self.active_meeting_slice -= 1
            self.update_content_frame()

    def to_prior_meeting(self, *e):
        if self.active_meeting_slice < 7:
            self.active_meeting_slice += 1
            self.update_content_frame()

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
        self.btn_next.configure(state=State.DISABLE)
        self.btn_prior.configure(state=State.DISABLE)

        if option_key in ['Jockey', 'Trainer']:
            if 'Earning' in option_value:
                self.build_earning_content(option_key, option_value)
            elif 'Meeting' in option_value:
                self.btn_next.configure(state=State.NORMAL)
                self.btn_prior.configure(state=State.NORMAL)
                self.build_meeting_performance_content(option_key)
        else:
            Label(
                self.content_frame,
                text=f'{option_key} / {option_value}',
                font='Times 14',
            ).pack()

    def build_earning_content(
        self,
        option_key: str,
        option_value: str,
    ):
        season = option_value.split(' ')[1]
        person_type = option_key.lower()
        earnings = Cache.get_earnings_by_season(person_type, season)
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
                if header == 'person' and value in IGNORED_PEOPLE:
                    break

                Label(self.content_frame, text=value, font=BODY_FONT,
                      fg=self.get_earning_color(person_type, header.lower(), value)) \
                    .grid(row=row, column=1 + headers.index(header), padx=6)

    @staticmethod
    def get_earning_color(person_type: str, field: str, value: str) -> str:
        if 'rich' in field:
            if (person_type == 'jockey' and float(value) >= 0.4) or \
                (person_type == 'trainer' and float(value) >= 0.3):
                return Color.ORANGE

        elif 'earndayavg' in field:
            if (person_type == 'jockey' and float(value) >= 12) or \
                (person_type == 'trainer' and float(value) >= 11):
                return Color.RED

        return Color.BLACK

    def build_meeting_performance_content(self, option_key: str):
        person_type = option_key.lower()
        performance = Cache.get_performance_by_meeting(person_type)
        persons = []
        placings = {
            'wins': 'W',
            'seconds': 'Q',
            'thirds': 'P',
            'fourths': 'F',
            'engagements': 'E',
        }

        for p in performance:
            for d in p['data']:
                name = d['person']
                if person_type == 'jockey' and name in JOCKEY_RANKINGS:
                    persons.append((name, JOCKEY_RANKINGS.index(name)))
                elif person_type == 'trainer' and name in TRAINER_RANKINGS:
                    persons.append((name, TRAINER_RANKINGS.index(name)))

        persons = sorted(persons, key=itemgetter(1))
        for p in persons:
            Label(self.content_frame, text=p[0], font=BODY_FONT) \
                .grid(row=2 + persons.index(p), column=1, padx=15)

        actives = performance[self.active_meeting_slice:]
        for m in actives:
            index = actives.index(m)
            col = 2 + index
            if index > 2:
                break

            header = f'{m["meeting"]} {m["venue"]} ' \
                     f'{m["races"]}R  ${m["turnover"]}'
            Label(self.content_frame, text=header, font=HEADER_FONT) \
                .grid(row=1, column=col, padx=15, pady=2)

            for p in persons:
                row = 2 + persons.index(p)
                for d in m['data']:
                    if d['person'] != p[0]:
                        continue

                    frame = Frame(self.content_frame)
                    for k, v in placings.items():
                        text = f'{d[k]}{v}' if d[k] != 0 else ''
                        column = [x for x in placings.keys()].index(k)
                        color = self.get_performance_color(text)
                        Label(frame, text=text, font=BODY_FONT, fg=color) \
                            .grid(row=1, column=1 + column, padx=2)

                    earnings = f'${d["earnings"]}' if d['earnings'] > 0 else ''
                    Label(frame, text=earnings, font=BODY_FONT) \
                        .grid(row=1, column=1 + len(placings), padx=2)
                    frame.grid(row=row, column=col, padx=15)

    @staticmethod
    def get_performance_color(text: str) -> str:
        if 'W' in text:
            return Color.GOLD
        elif 'Q' in text:
            return Color.SILVER
        elif 'P' in text:
            return Color.BROWN

        return Color.BLACK
