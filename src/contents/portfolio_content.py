from tkinter import Frame, Label

from src.storage.storage import Storage
from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.utils.roi import ROI
from src.utils.constants import \
    Race, Tip, Pool, Misc, Color, ROI_RANGE, MessageLevel


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
        self.tips = None
        self.odds = None
        self.dividends = None
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
        self.tips, self.odds, self.dividends = \
            race[Race.TIPS], race[Race.ODDS], race[Race.DIVIDENDS]

        if len(self.tips) == 0:
            self.set_message(MessageLevel.INFO, 'No tips found.')
            return

        self.build_header()
        self.build_body()
        self.nested_frame.pack()

    def build_header(self):
        header_font = 'Times 16 bold'
        for i in range(1, 5):
            Label(self.nested_frame, text=Misc.ORDINALS[i], font=header_font) \
                .grid(row=1, column=2 + i, padx=10, pady=5)

        Label(self.nested_frame, text='') \
            .grid(row=1, column=2 + 4 + 1, padx=10, pady=5)

        pools = [Pool.WIN, Pool.QPL, Pool.QIN, Pool.FCT]
        for pool in pools:
            index = 1 + pools.index(pool)
            Label(self.nested_frame, text=pool, font=header_font) \
                .grid(row=1, column=2 + 4 + 1 + index, padx=10, pady=5)

    def build_body(self):
        groups = {}
        for t in self.tips:
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

                Label(
                    self.nested_frame,
                    text=tipster,
                    font='Times 14 bold',
                    fg=Color.BLUE if t[Tip.CONFIDENT] else Color.BLACK
                ).grid(row=row, column=2, padx=20, pady=3)

                for h in t[Tip.TIP]:
                    col = 3 + t[Tip.TIP].index(h)
                    Label(
                        self.nested_frame,
                        text=str(h),
                        font=f'Times 14 {self.get_horse_num_font(h)}',
                        fg=self.get_horse_num_color(h),
                    ).grid(row=row, column=col, padx=10, pady=3)

                rois = ROI.get_return_on_investments(
                    self.odds, self.dividends, t[Tip.TIP]
                )
                for pool, roi_pair in rois.items():
                    col = 8 + [k for k in rois.keys()].index(pool)
                    roi_text = f'{roi_pair[0] if roi_pair[0] is not None else 0}'
                    if roi_pair[1] is not None:
                        roi_text += f' [{roi_pair[1]}]'

                    Label(
                        self.nested_frame,
                        text=roi_text,
                        font='Times 14',
                        fg=self.get_roi_color(pool, roi_text)
                    ).grid(row=row, column=col, padx=15, pady=3)

            tips_count += len(tips_list)

    def get_roi_color(self, pool: str, roi_text: str) -> str:
        # know the result and won
        if '[' in roi_text:
            actual_roi = roi_text.split(' ')[1].replace('[', '').replace(']', '')
            return Color.GREEN if float(actual_roi) > 0 else Color.RED

        # don't know the result yet
        if Pool.WIN not in self.dividends:
            roi_range = ROI_RANGE[pool]
            if roi_range[0] <= float(roi_text) <= roi_range[1]:
                return Color.GREEN

        return Color.BLACK

    def get_horse_num_font(self, horse_num: int) -> str:
        if self.is_winner(horse_num) or self.is_second(horse_num):
            return 'bold underline'
        elif self.is_fourth(horse_num):
            return 'bold'
        return ''

    def get_horse_num_color(self, horse_num: int) -> str:
        if self.is_winner(horse_num):
            return Color.GOLD
        elif self.is_second(horse_num):
            return Color.SILVER
        elif self.is_third(horse_num):
            return Color.BROWN
        return Color.BLACK

    def is_winner(self, horse_num: int):
        return Pool.WIN in self.dividends and \
               str(horse_num) in self.dividends[Pool.WIN]

    def is_second(self, horse_num: int):
        return Pool.QTT in self.dividends and \
               horse_num == self.dividends[Pool.QTT][0][Race.COMBINATION][1]

    def is_third(self, horse_num: int):
        return Pool.QTT in self.dividends and \
               horse_num == self.dividends[Pool.QTT][0][Race.COMBINATION][2]

    def is_fourth(self, horse_num: int):
        return Pool.QTT in self.dividends and \
               horse_num == self.dividends[Pool.QTT][0][Race.COMBINATION][3]
