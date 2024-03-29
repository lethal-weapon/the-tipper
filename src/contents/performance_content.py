from operator import itemgetter
from tkinter import Frame, Label, LEFT, \
    Radiobutton, Checkbutton, StringVar, IntVar

from src.ui.dropdown import Dropdown
from src.contents.content import Content
from src.storage.cache import Cache
from src.utils.constants import \
    Color, IGNORED_PEOPLE, JOCKEY_RANKINGS, TRAINER_RANKINGS

PAGE_OPTIONS = {
    'Tipster': [
        'Last day',
        'All times',
    ],
    'Jockey': [
        'Earning 22/23',
        'Earning 21/22',
        'Meeting',
    ],
    'Trainer': [
        'Earning 22/23',
        'Earning 21/22',
        'Meeting',
    ],
}

HEADER_FONT = 'Times 14 bold'
BODY_FONT = 'Times 13'
BODY_FONT_BOLD = f'{BODY_FONT} bold'
BODY_FONT_UNDERLINE = f'{BODY_FONT} underline'
BODY_FONT_EMPHASIS = f'{BODY_FONT} bold underline'


class PerformanceContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.header_frame = Frame(self.frame)
        self.option_key = StringVar()
        self.option_list = None
        self.cached = IntVar(value=1)
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

        Label(
            self.header_frame,
            text='Cached',
            font='Times 16 italic',
            fg=Color.BLUE,
        ).pack(padx=20, side=LEFT)
        Checkbutton(
            self.header_frame,
            variable=self.cached,
        ).pack(side=LEFT)

    def to_clear_cache(self) -> bool:
        return self.cached.get() == 0

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
        self.content_frame.pack(pady=7)

    def build_content_frame(self):
        option_key, option_value = \
            self.option_key.get(), self.option_list.get_selected_option()

        if option_key in ['Jockey', 'Trainer']:
            if 'Earning' in option_value:
                self.build_earning_content(option_key, option_value)
            elif 'Meeting' in option_value:
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
        earnings = Cache \
            .get_earnings_by_season(self.to_clear_cache(), person_type, season)
        headers = []

        if len(earnings) > 0:
            headers = [k for k in earnings[0].keys()]

        for header in headers:
            formatted_header = header[0].upper() + header[1:]
            Label(self.content_frame, text=formatted_header, font=HEADER_FONT) \
                .grid(row=1, column=1 + headers.index(header), padx=6, pady=5)

        row = 1
        for earning in earnings:
            row += 1
            for header in headers:
                value = str(earning[header])
                if header == 'person' and value in IGNORED_PEOPLE:
                    break

                Label(self.content_frame, text=value, font=BODY_FONT,
                      fg=self.get_earning_color(person_type, header.lower(), value)) \
                    .grid(row=row, column=1 + headers.index(header), padx=6, pady=2)

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
        performance = Cache \
            .get_performance_by_meeting(self.to_clear_cache(), person_type)
        persons = []
        placings = [
            ('wins', 'W'),
            ('seconds', 'Q'),
            ('thirds', 'P'),
            ('fourths', 'F'),
            ('engagements', 'E'),
            ('earnings', '$'),
        ]

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
                .grid(row=3 + persons.index(p), column=1, padx=15, pady=2)

        for m in performance:
            index = performance.index(m)
            col = 2 + index * len(placings)
            if index > 4:
                break

            header = f'{m["meeting"]} {m["venue"]} ' \
                     f'{m["races"]}R  ${m["turnover"]}'
            Label(self.content_frame, text=header, font=HEADER_FONT) \
                .grid(row=1, column=col, columnspan=len(placings), padx=15)

            for tp in placings:
                font, color = self.get_performance_font_and_color(tp[1])
                Label(self.content_frame, text=tp[1], font=font, fg=color) \
                    .grid(row=2, column=col + placings.index(tp))

            for p in persons:
                row = 3 + persons.index(p)
                for d in m['data']:
                    if d['person'] != p[0]:
                        continue

                    for tp in placings:
                        if tp[1] in ['E', '$']:
                            earns = None
                            text = f'{d[tp[0]]}' if d[tp[0]] != 0 else ''
                        else:
                            earns = [pe['earning'] for pe in d[tp[0]]]
                            count = len(earns)
                            text = f'{count}' if count != 0 else ''

                        font, color = self.get_performance_font_and_color(tp[1], text, earns)
                        Label(self.content_frame, text=text, font=font, fg=color) \
                            .grid(row=row, column=col + placings.index(tp))

    @staticmethod
    def get_performance_font_and_color(
        kind: str,
        count: str = '',
        earns: [float] = None,
    ) -> (str, str):
        font, color = BODY_FONT_BOLD, Color.BLACK
        if kind == 'W':
            color = Color.GOLD
        elif kind == 'Q':
            color = Color.SILVER
        elif kind == 'P':
            color = Color.BROWN

        if len(count) > 0:
            if (kind == '$' and float(count) >= 12) or \
                (kind == 'W' and int(count) >= 2) or \
                (kind in ['Q', 'P', 'F'] and int(count) >= 3):
                font = BODY_FONT_EMPHASIS

        if earns:
            if (kind == 'W' and len(list(filter(lambda e: e >= 12, earns))) > 0) or \
                (kind in ['Q', 'P', 'F'] and len(list(filter(lambda e: e >= 4, earns))) > 0):
                font = BODY_FONT_EMPHASIS

        return font, color
