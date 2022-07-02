from tkinter import Frame, Label

from src.storage.storage import Storage
from src.contents.content import Content
from src.ui.race_selector import RaceSelector
from src.utils.constants import \
    Race, Tip, Pool, Misc, Color, ROI_MAPPER, MessageLevel


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

        pools = ['WIN', 'QIN', 'FCT']
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

                for at in t[Tip.TIP]:
                    col = 3 + t[Tip.TIP].index(at)
                    Label(self.nested_frame, text=str(at), font='Times 14') \
                        .grid(row=row, column=col, padx=10, pady=3)

                horse_nums = [str(n) for n in sorted(t[Tip.TIP])]
                rois = self.get_return_on_investment(horse_nums)
                for pool, roi in rois.items():
                    col = 8 + [k for k in rois.keys()].index(pool)
                    Label(
                        self.nested_frame,
                        text=str(roi),
                        font='Times 14',
                        fg=Color.RED if roi < ROI_MAPPER[pool] else Color.GREEN
                    ).grid(row=row, column=col, padx=10, pady=3)

            tips_count += len(tips_list)

    def get_return_on_investment(self, tips: [str]) -> dict:
        return {
            Pool.WIN: self.get_win_roi(tips),
            Pool.QIN: self.get_qin_roi(tips),
            Pool.FCT: self.get_fct_roi(tips),
        }

    def get_win_roi(self, tips: [str]) -> float:
        if Pool.WIN_PLA not in self.odds:
            return 0

        odds_list = []
        for h in tips:
            if h in self.odds[Pool.WIN_PLA]:
                odds_list.append(self.odds[Pool.WIN_PLA][h][0])

        return \
            round(sum(odds_list) / len(odds_list) - len(odds_list), 1)

    def get_qin_roi(self, tips: [str]) -> int:
        if Pool.QIN not in self.odds:
            return 0

        odds_list = []
        for i in range(len(tips) - 1):
            for j in range(i + 1, len(tips)):
                horse_1, horse_2 = tips[i], tips[j]

                if horse_1 in self.odds[Pool.QIN] and \
                    horse_2 in self.odds[Pool.QIN][horse_1]:
                    odds_list.append(self.odds[Pool.QIN][horse_1][horse_2])

        return \
            int(sum(odds_list) / len(odds_list) - len(odds_list))

    def get_fct_roi(self, tips: [str]) -> int:
        if Pool.FCT not in self.odds:
            return 0

        odds_list = []
        for i in range(len(tips)):
            for j in range(len(tips)):
                if i == j:
                    continue
                horse_1, horse_2 = tips[i], tips[j]

                if horse_1 in self.odds[Pool.FCT] and \
                    horse_2 in self.odds[Pool.FCT][horse_1]:
                    odds_list.append(self.odds[Pool.FCT][horse_1][horse_2])

        return \
            int(sum(odds_list) / len(odds_list) - len(odds_list))
