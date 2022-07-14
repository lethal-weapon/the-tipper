from src.storage.storage import Storage
from src.analysis.roi import ROI
from src.utils.constants import Race, Pool, Tip
from src.utils.tipster_sources import TIPSTER_SOURCES

MIN_OPTIMIZED_RACES = len(Storage.get_race_dates())


class ROIRange:
    rois: dict = {}
    performance: dict = {}
    tops: dict = {}

    @classmethod
    def initialize(cls):
        cls.build_rois()
        cls.build_performance()
        cls.build_tops()

    @classmethod
    def get_ideal_range(cls, tip_obj: dict, pool: str) -> (int, int):
        sorted_pool_top_list = cls.tops[pool]
        person = f'{tip_obj[Tip.SOURCE]}/{tip_obj[Tip.TIPSTER]}'

        for (p, s, r, b) in sorted_pool_top_list:
            if p == person and sorted_pool_top_list.index((p, s, r, b)) < 4:
                return b

        return -99, -99

    @classmethod
    def build_rois(cls):
        for (race_date, race_num) in Storage.get_race_tuples():
            race = Storage.get_race(race_date, race_num)
            odds, dividends = race[Race.ODDS], race[Race.DIVIDENDS]
            if len(odds) < 1 or len(dividends) < 1:
                continue

            for source, tipsters in TIPSTER_SOURCES.items():
                for tipster in tipsters:
                    person = f'{source}/{tipster}'
                    tip_obj = Storage.get_tip(race_date, race_num, source, tipster)
                    if not tip_obj:
                        continue

                    tip = tip_obj[Tip.TIP]
                    raw_roi = \
                        ROI.get_return_on_investments(odds, dividends, tip)

                    correct_roi = {}
                    for pool, roi_pair in raw_roi.items():
                        if roi_pair[1] is not None:
                            correct_roi[pool] = roi_pair
                            continue
                        if pool == Pool.WIN:
                            correct_roi[pool] = (roi_pair[0], -len(tip))
                        elif pool == Pool.QIN or pool == Pool.QPL:
                            correct_roi[pool] = (roi_pair[0], -(len(tip) * (len(tip) - 1) // 2))
                        elif pool == Pool.FCT:
                            correct_roi[pool] = (roi_pair[0], -(len(tip) * (len(tip) - 1)))

                    if person in cls.rois:
                        cls.rois[person].append(correct_roi)
                    else:
                        cls.rois[person] = [correct_roi]

    @classmethod
    def build_performance(cls):
        for person, roi_list in cls.rois.items():
            cls.performance[person] = {}

            for pool in roi_list[0].keys():
                best_pool_potential_roi_range = (1, 200)
                best_pool_score = 0
                best_races = 0

                for i in range(5, 200):
                    for j in range(i + 5, 200, 5):
                        races = range_score = 0

                        for roi in roi_list:
                            for p, pair in roi.items():
                                if p == pool and (i <= pair[0] <= j):
                                    races += 1
                                    range_score += pair[1]

                        if range_score > best_pool_score:
                            best_races = races
                            best_pool_score = range_score
                            best_pool_potential_roi_range = (i, j)

                cls.performance[person][pool] = \
                    f'{best_pool_score}/{best_races}/{best_pool_potential_roi_range}'

    @classmethod
    def build_tops(cls):
        for person, nested_rois in cls.performance.items():
            for pool, roi in nested_rois.items():
                if pool not in cls.tops:
                    cls.tops[pool] = []

                slices = roi.split('/')
                score, races = float(slices[0]), int(slices[1])
                nested_slices = slices[2] \
                    .replace('(', '').replace(')', '').replace(' ', '').split(',')
                lower, upper = int(nested_slices[0]), int(nested_slices[1])

                if races < MIN_OPTIMIZED_RACES:
                    continue

                index = 0
                for (p, s, r, b) in cls.tops[pool]:
                    if races == 0 or r == 0:
                        index = len(cls.tops[pool])
                        break
                    if (score / races) < (s / r):
                        index += 1
                cls.tops[pool].insert(index, (person, score, races, (lower, upper)))
