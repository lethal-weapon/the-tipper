import webbrowser
from tkinter import Frame, Label, LEFT

from src.storage.storage import Storage
from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.analysis.roi import ROI, MIN_ROI_WIN_ODDS
from src.analysis.roi_range import ROIRange
from src.utils.constants import Race, Tip, Pool, Misc, Color


class PortfolioContent(Content):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.header_frame = Frame(self.frame)
        self.race_picker = None
        self.build_page_header()
        self.header_frame.pack()

        self.content_frame = Frame(self.frame)
        self.tips = None
        self.odds = None
        self.dividends = None
        self.refresh_frame = None

        self.refresh()
        self.content_frame.pack()
        self.pack_message()
        self.frame.pack()

    def build_page_header(self):
        self.race_picker = RaceSelector(
            self.header_frame,
            self.refresh,
            Storage.get_race_date_and_num_count(),
            10,
            LEFT
        )
        result_link = Label(
            self.header_frame,
            text='Result',
            font='Times 16 underline',
            cursor='hand2',
        )
        video_link = Label(
            self.header_frame,
            text='Replay',
            font='Times 16 underline',
            cursor='hand2',
        )
        result_link.bind('<Button-1>', self.open_race_result_page)
        video_link.bind('<Button-1>', self.play_race_replay)
        result_link.pack(padx=15, side=LEFT)
        video_link.pack(side=LEFT)

    def play_race_replay(self, *e):
        race_date, race_num = self.race_picker.get_race_date_num()
        video_url = Storage.get_race(race_date, race_num)[Race.VIDEO_URL]
        webbrowser.open_new_tab(video_url)

    def open_race_result_page(self, *e):
        race_date, race_num = self.race_picker.get_race_date_num()
        result_url = Storage.get_race(race_date, race_num)[Race.RESULT_URL]
        webbrowser.open_new_tab(result_url)

    def refresh(self):
        """ Recreate the content according to the race date/num. """
        if self.refresh_frame:
            self.refresh_frame.pack_forget()
            self.refresh_frame.destroy()

        self.refresh_frame = Frame(self.content_frame)
        self.clear_message()

        if Storage.is_empty():
            self.set_info_message('No race found.')
            return

        race_date, race_num = self.race_picker.get_race_date_num()
        race = Storage.get_race(race_date, race_num)
        self.tips, self.odds, self.dividends = \
            race[Race.TIPS], race[Race.ODDS], race[Race.DIVIDENDS]

        if len(self.tips) == 0:
            self.set_info_message('No tips found.')
            return

        self.build_content_header()
        self.build_content_body()
        self.refresh_frame.pack()

    def build_content_header(self):
        header_font = 'Times 16 bold'
        for i in range(1, 5):
            Label(self.refresh_frame, text=Misc.ORDINALS[i], font=header_font) \
                .grid(row=1, column=2 + i, padx=10, pady=5)

        Label(self.refresh_frame, text='') \
            .grid(row=1, column=2 + 4 + 1, padx=10, pady=5)

        pools = [Pool.WIN, Pool.QPL, Pool.QIN, Pool.FCT]
        for pool in pools:
            index = 1 + pools.index(pool)
            Label(self.refresh_frame, text=pool, font=header_font) \
                .grid(row=1, column=2 + 4 + 1 + index, padx=10, pady=5)

    def build_content_body(self):
        groups = {}
        for t in self.tips:
            if t[Tip.SOURCE] in groups:
                groups[t[Tip.SOURCE]].append(t)
            else:
                groups[t[Tip.SOURCE]] = [t]

        tips_count = 0
        for source, unsorted_tips_list in groups.items():
            Label(self.refresh_frame, text=source, font='Times 14 italic') \
                .grid(row=2 + tips_count, column=1, padx=10, pady=3)

            tips_list = sorted(unsorted_tips_list, key=lambda d: d[Tip.TIPSTER])
            for t in tips_list:
                tipster = t[Tip.TIPSTER].split(' ')[0]
                row = 2 + tips_count + tips_list.index(t)

                Label(
                    self.refresh_frame,
                    text=tipster,
                    font='Times 14 bold',
                    fg=Color.BLUE if t[Tip.CONFIDENT] else Color.BLACK
                ).grid(row=row, column=2, padx=20, pady=3)

                for h in t[Tip.TIP]:
                    col = 3 + t[Tip.TIP].index(h)
                    Label(
                        self.refresh_frame,
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
                        self.refresh_frame,
                        text=roi_text,
                        font='Times 14',
                        fg=self.get_roi_color(t, pool, roi_text)
                    ).grid(row=row, column=col, padx=15, pady=3)

            tips_count += len(tips_list)

    def get_roi_color(
        self,
        tip_obj: dict,
        pool: str,
        roi_text: str
    ) -> str:
        # know the result and won
        if '[' in roi_text:
            actual_roi = roi_text.split(' ')[1].replace('[', '').replace(']', '')
            return Color.GREEN if float(actual_roi) > 0 else Color.RED

        # don't know the result yet
        if Pool.WIN not in self.dividends:
            roi_range = ROIRange.get_ideal_range(tip_obj, pool)
            if roi_range[0] <= float(roi_text) <= roi_range[1]:
                return Color.GREEN

        return Color.BLACK

    def get_horse_num_font(self, horse_num: int) -> str:
        if Pool.WIN in self.dividends:
            if self.is_winner(horse_num) or self.is_second(horse_num):
                return 'bold underline'
            elif self.is_fourth(horse_num):
                return 'bold'
        return ''

    def get_horse_num_color(self, horse_num: int) -> str:
        # highlight horses with high win odds before having the result
        if (Pool.WIN not in self.dividends) and Pool.WIN_PLA in self.odds:
            num_str = str(horse_num)
            if num_str in self.odds[Pool.WIN_PLA]:
                win_odds = self.odds[Pool.WIN_PLA][num_str][0]
                if win_odds >= MIN_ROI_WIN_ODDS:
                    return Color.ORANGE

        if Pool.WIN in self.dividends:
            if self.is_winner(horse_num):
                return Color.GOLD
            elif self.is_second(horse_num):
                return Color.SILVER
            elif self.is_third(horse_num):
                return Color.BROWN

        return Color.BLACK

    def is_winner(self, horse_num: int):
        return str(horse_num) in self.dividends[Pool.WIN]

    def is_second(self, horse_num: int):
        return horse_num == self.dividends[Pool.QTT][0][Race.COMBINATION][1]

    def is_third(self, horse_num: int):
        return horse_num == self.dividends[Pool.QTT][0][Race.COMBINATION][2]

    def is_fourth(self, horse_num: int):
        return horse_num == self.dividends[Pool.QTT][0][Race.COMBINATION][3]
