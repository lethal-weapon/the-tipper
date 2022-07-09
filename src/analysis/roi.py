from src.utils.constants import Race, Pool


class ROI:

    @classmethod
    def get_return_on_investments(
        cls,
        odds: dict,
        dividends: dict,
        tips: [int]
    ) -> dict:
        return {
            Pool.WIN: cls.get_win_roi(odds, dividends, tips),
            Pool.QPL: cls.get_qpl_roi(odds, dividends, tips),
            Pool.QIN: cls.get_qin_roi(odds, dividends, tips),
            Pool.FCT: cls.get_fct_roi(odds, dividends, tips),
        }

    @classmethod
    def get_win_roi(cls, odds, dividends, tips: [int]) -> (float, float):
        potential_roi = actual_roi = None
        tips_str = [str(t) for t in tips]
        odds_list, actual_win_odds = [], 0

        for t in tips_str:
            if (Pool.WIN_PLA in odds) and (t in odds[Pool.WIN_PLA]):
                odds_list.append(odds[Pool.WIN_PLA][t][0])

            if (Pool.WIN in dividends) and (t in dividends[Pool.WIN]):
                actual_win_odds += dividends[Pool.WIN][t]

        if len(odds_list) > 0:
            potential_roi = \
                round(sum(odds_list) / len(odds_list) - len(odds_list), 1)
            if actual_win_odds != 0:
                actual_roi = \
                    round(actual_win_odds - len(odds_list), 1)

        return potential_roi, actual_roi

    @classmethod
    def get_qpl_roi(cls, odds, dividends, tips: [int]) -> (int, int):
        return cls.get_qqp_roi(odds, dividends, Pool.QPL, tips)

    @classmethod
    def get_qin_roi(cls, odds, dividends, tips: [int]) -> (int, int):
        return cls.get_qqp_roi(odds, dividends, Pool.QIN, tips)

    @classmethod
    def get_qqp_roi(cls, odds, dividends, pool, tips: [int]) -> (int, int):
        potential_roi = actual_roi = None
        sorted_tips = [str(t) for t in sorted(tips)]
        odds_list, actual_qqp_odds = [], 0

        for i in range(len(sorted_tips) - 1):
            for j in range(i + 1, len(sorted_tips)):
                horse_1, horse_2 = sorted_tips[i], sorted_tips[j]
                if horse_1 == horse_2:
                    continue

                if pool in odds and \
                    horse_1 in odds[pool] and \
                    horse_2 in odds[pool][horse_1]:
                    odds_list.append(odds[pool][horse_1][horse_2])

                if pool in dividends:
                    for comb in dividends[pool]:
                        if int(horse_1) in comb[Race.COMBINATION] and \
                            int(horse_2) in comb[Race.COMBINATION]:
                            actual_qqp_odds += comb[Race.ODDS]

        if len(odds_list) > 0:
            potential_roi = \
                int(sum(odds_list) / len(odds_list) - len(odds_list))
            if actual_qqp_odds != 0:
                actual_roi = \
                    int(actual_qqp_odds - len(odds_list))

        return potential_roi, actual_roi

    @classmethod
    def get_fct_roi(cls, odds, dividends, tips: [int]) -> (int, int):
        potential_roi = actual_roi = None
        sorted_tips = [str(t) for t in sorted(tips)]
        odds_list, actual_fct_odds = [], 0

        for i in range(len(sorted_tips)):
            for j in range(len(sorted_tips)):
                horse_1, horse_2 = sorted_tips[i], sorted_tips[j]
                if horse_1 == horse_2:
                    continue

                if Pool.FCT in odds and \
                    horse_1 in odds[Pool.FCT] and \
                    horse_2 in odds[Pool.FCT][horse_1]:
                    odds_list.append(odds[Pool.FCT][horse_1][horse_2])

                if Pool.FCT in dividends:
                    for comb in dividends[Pool.FCT]:
                        if int(horse_1) == comb[Race.COMBINATION][0] and \
                            int(horse_2) == comb[Race.COMBINATION][1] and \
                            comb[Race.ODDS] > actual_fct_odds:
                            actual_fct_odds = comb[Race.ODDS]

        if len(odds_list) > 0:
            potential_roi = \
                int(sum(odds_list) / len(odds_list) - len(odds_list))
            if actual_fct_odds != 0:
                actual_roi = \
                    int(actual_fct_odds - len(odds_list))

        return potential_roi, actual_roi
