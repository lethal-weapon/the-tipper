from tkinter import Frame, Label

from src.storage.storage import Storage
from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.utils.constants import Race, Tip, Misc, Style, Color, MessageLevel


class PortfolioContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.race_picker = RaceSelector(
            self.frame,
            self.refresh,
            Storage.get_race_date_and_num_count(),
            10
        )
        self.content_frame = Frame(self.frame)
        self.nested_frame = None

        self.refresh()
        self.content_frame.pack()
        self.pack_message()
        self.frame.pack()

    def refresh(self):
        """ Recreate the contents according to the race date/num. """
        if self.nested_frame:
            self.nested_frame.pack_forget()
            self.nested_frame.destroy()

        self.nested_frame = Frame(self.content_frame)
        self.clear_message()

        if Storage.is_empty():
            self.set_message(MessageLevel.INFO, 'No race found.')
            return

        race_date, race_num = self.race_picker.get_race_date_num()
        race = Storage.get_race(race_date, race_num)
        tips = race[Race.TIPS]

        if len(tips) == 0:
            self.set_message(MessageLevel.INFO, 'No tips found.')
            return

        self.build_header()
        self.build_body(tips)
        self.nested_frame.pack()

    def build_header(self):
        header_font = 'Times 16 bold'
        for i in range(1, 5):
            Label(self.nested_frame, text=Misc.ORDINALS[i], font=header_font) \
                .grid(row=1, column=2 + i, padx=10, pady=5)

        Label(self.nested_frame, text='') \
            .grid(row=1, column=2 + 4 + 1, padx=10, pady=5)

        pools = ['WIN', 'QIN', 'FCT']
        for pool in pools:
            index = 1 + pools.index(pool)
            Label(self.nested_frame, text=pool, font=header_font) \
                .grid(row=1, column=2 + 4 + 1 + index, padx=10, pady=5)

    def build_body(self, tips: [dict]):
        groups = {}
        for t in tips:
            if t[Tip.SOURCE] in groups:
                groups[t[Tip.SOURCE]].append(t)
            else:
                groups[t[Tip.SOURCE]] = [t]

        tips_count = 0
        for source, unsorted_tips_list in groups.items():
            Label(self.nested_frame, text=source, font='Times 14 italic') \
                .grid(row=2 + tips_count, column=1, padx=10, pady=3)

            tips_list = sorted(unsorted_tips_list, key=lambda d: d[Tip.TIPSTER])
            for t in tips_list:
                tipster = t[Tip.TIPSTER].split(' ')[0]
                row = 2 + tips_count + tips_list.index(t)

                tipster_label = \
                    Label(self.nested_frame, text=tipster, font='Times 14 bold')
                if t[Tip.CONFIDENT]:
                    tipster_label.__setitem__(Style.FG, Color.BLUE)
                tipster_label.grid(row=row, column=2, padx=20, pady=3)

                for at in t[Tip.TIP]:
                    col = 3 + t[Tip.TIP].index(at)
                    Label(self.nested_frame, text=str(at), font='Times 14') \
                        .grid(row=row, column=col, padx=10, pady=3)

            tips_count += len(tips_list)
