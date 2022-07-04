from tkinter import Frame, Label

from src.storage.storage import Storage
from src.contents.content import Content
from src.ui.race_selector import RaceSelector
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

        pools = [Pool.WIN, Pool.QIN, Pool.FCT]
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

                horse_nums = [str(h) for h in t[Tip.TIP]]
                rois = self.get_return_on_investment(horse_nums)
                for pool, roi in rois.items():
                    col = 8 + [k for k in rois.keys()].index(pool)
                    Label(
                        self.nested_frame,
                        text=str(roi),
                        font='Times 14',
                        fg=self.get_roi_color(pool, str(roi))
                    ).grid(row=row, column=col, padx=15, pady=3)

            tips_count += len(tips_list)

    def get_roi_color(self, pool: str, roi: str) -> str:
        # know the result and won
        if '[' in roi:
            actual_roi = roi.split(' ')[1].replace('[', '').replace(']', '')
            return Color.GREEN if float(actual_roi) > 0 else Color.RED

        # don't know the result yet
        if Pool.WIN not in self.dividends:
            roi_range = ROI_RANGE[pool]
            if roi_range[0] <= float(roi) <= roi_range[1]:
                return Color.GREEN

        return Color.BLACK

    def get_horse_num_font(self, horse_num: int) -> str:
        if self.is_winner(horse_num) or self.is_second(horse_num):
            return 'bold underline'
        return ''

    def get_horse_num_color(self, horse_num: int) -> str:
        if self.is_winner(horse_num):
            return Color.GOLD
        elif self.is_second(horse_num):
            return Color.SILVER
        return Color.BLACK

    def is_winner(self, horse_num: int):
        return Pool.WIN in self.dividends and \
               str(horse_num) in self.dividends[Pool.WIN]

    def is_second(self, horse_num: int):
        return Pool.FCT in self.dividends and \
               horse_num in self.dividends[Pool.FCT][0][Race.COMBINATION]

    def get_return_on_investment(self, tips: [str]) -> dict:
        return {
            Pool.WIN: self.get_win_roi(tips),
            Pool.QIN: self.get_qin_roi(tips),
            Pool.FCT: self.get_fct_roi(tips),
        }

    def get_win_roi(self, tips: [str]):
        if Pool.WIN_PLA not in self.odds:
            return 0

        odds_list = []
        actual_win_odds = 0

        for t in tips:
            if t in self.odds[Pool.WIN_PLA]:
                odds_list.append(self.odds[Pool.WIN_PLA][t][0])

            if Pool.WIN in self.dividends and \
                t in self.dividends[Pool.WIN] and \
                self.dividends[Pool.WIN][t] > actual_win_odds:
                actual_win_odds = self.dividends[Pool.WIN][t]

        potential_roi = \
            round(sum(odds_list) / len(odds_list) - len(odds_list), 1)
        actual_roi = \
            round(actual_win_odds - len(odds_list), 1)

        if actual_win_odds == 0:
            return potential_roi
        else:
            return f'{potential_roi} [{actual_roi}]'

    def get_qin_roi(self, tips: [str]):
        if Pool.QIN not in self.odds:
            return 0

        sorted_tips = [str(h) for h in sorted([int(t) for t in tips])]
        odds_list = []
        actual_qin_odds = 0

        for i in range(len(sorted_tips) - 1):
            for j in range(i + 1, len(sorted_tips)):
                horse_1, horse_2 = sorted_tips[i], sorted_tips[j]
                if horse_1 == horse_2:
                    continue

                if horse_1 in self.odds[Pool.QIN] and \
                    horse_2 in self.odds[Pool.QIN][horse_1]:
                    odds_list.append(self.odds[Pool.QIN][horse_1][horse_2])

                if Pool.QIN in self.dividends:
                    for comb in self.dividends[Pool.QIN]:
                        if int(horse_1) in comb[Race.COMBINATION] and \
                            int(horse_2) in comb[Race.COMBINATION] and \
                            comb[Race.ODDS] > actual_qin_odds:
                            actual_qin_odds = comb[Race.ODDS]

        potential_roi = \
            int(sum(odds_list) / len(odds_list) - len(odds_list))
        actual_roi = \
            int(actual_qin_odds - len(odds_list))

        if actual_qin_odds == 0:
            return potential_roi
        else:
            return f'{potential_roi} [{actual_roi}]'

    def get_fct_roi(self, tips: [str]):
        if Pool.FCT not in self.odds:
            return 0

        sorted_tips = [str(h) for h in sorted([int(t) for t in tips])]
        odds_list = []
        actual_fct_odds = 0

        for i in range(len(sorted_tips)):
            for j in range(len(sorted_tips)):
                horse_1, horse_2 = sorted_tips[i], sorted_tips[j]
                if horse_1 == horse_2:
                    continue

                if horse_1 in self.odds[Pool.FCT] and \
                    horse_2 in self.odds[Pool.FCT][horse_1]:
                    odds_list.append(self.odds[Pool.FCT][horse_1][horse_2])

                if Pool.FCT in self.dividends:
                    for comb in self.dividends[Pool.FCT]:
                        if int(horse_1) in comb[Race.COMBINATION] and \
                            int(horse_2) in comb[Race.COMBINATION] and \
                            comb[Race.ODDS] > actual_fct_odds:
                            actual_fct_odds = comb[Race.ODDS]

        potential_roi = \
            int(sum(odds_list) / len(odds_list) - len(odds_list))
        actual_roi = \
            int(actual_fct_odds - len(odds_list))

        if actual_fct_odds == 0:
            return potential_roi
        else:
            return f'{potential_roi} [{actual_roi}]'
