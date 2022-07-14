from src.storage.storage import Storage
from src.analysis.roi import ROI
from src.utils.constants import Race, Pool, Tip
from src.utils.tipster_sources import TIPSTER_SOURCES

Storage.initialize()
MIN_OPTIMIZED_RACES = len(Storage.get_race_dates())

rois = {}


def build_rois():
    global rois
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

                if person in rois:
                    rois[person].append(correct_roi)
                else:
                    rois[person] = [correct_roi]


def run_raw_performance():
    global rois
    performance, counts = {}, {}

    for person, roi_list in rois.items():
        performance[person] = {}
        counts[person] = len(roi_list)

        for roi in roi_list:
            for pool, roi_pair in roi.items():
                if pool in performance[person]:
                    performance[person][pool] += roi_pair[1]
                else:
                    performance[person][pool] = roi_pair[1]

    print_raw_result(performance, counts)


def run_optimized_performance():
    global rois
    performance = {}

    for person, roi_list in rois.items():
        performance[person] = {}

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

            performance[person][pool] = \
                f'{best_pool_score}/{best_races}/{best_pool_potential_roi_range}'

    print_optimized_result(performance)
    print_optimized_tops(performance)


def print_raw_result(performance, count):
    print(f'-------------------------------------------------------------------------------')
    print(f'|         Tipster         |   Races   |   WIN   |   QPL   |   QIN   |   FCT   |')
    print(f'-------------------------------------------------------------------------------')
    lines = []
    for person, nested_rois in performance.items():
        line = '|  {}'.format(person)
        for i in range(26 - len(line)):
            line += ' '
        line += '{:>9}'.format(count[person])

        for pool, roi in nested_rois.items():
            line += '{:>10}'.format(int(roi))
        line += '   |'
        lines.append(line)

    for line in sorted(lines):
        print(line)
    print(f'-------------------------------------------------------------------------------')


def print_optimized_result(performance):
    print(f'------------------------------------------------------------------------------------------')
    print(f'|         Tipster         |      WIN      |      QPL      |      QIN      |      FCT     |')
    print(f'------------------------------------------------------------------------------------------')
    lines = []
    for person, nested_rois in performance.items():
        line = '|  {}'.format(person)
        for i in range(26 - len(line)):
            line += ' '

        for pool, roi in nested_rois.items():
            temp = [str(int(float(n)))
                    for n in roi
                    .replace('(', '').replace(')', '').replace(', ', '/').split('/')]
            line += '{:>15}'.format('-'.join(temp))
        line += '   |'
        lines.append(line)

    for line in sorted(lines):
        print(line)
    print(f'------------------------------------------------------------------------------------------')


def print_optimized_tops(performance):
    tops = {}

    for person, nested_rois in performance.items():
        for pool, roi in nested_rois.items():
            if pool not in tops:
                tops[pool] = []

            slices = roi.split('/')
            score, races = float(slices[0]), int(slices[1])
            nested_slices = slices[2] \
                .replace('(', '').replace(')', '').replace(' ', '').split(',')
            lower, upper = int(nested_slices[0]), int(nested_slices[1])

            if races < MIN_OPTIMIZED_RACES:
                continue

            index = 0
            for (p, s, r, b) in tops[pool]:
                if (score / races) < (s / r):
                    index += 1
            tops[pool].insert(index, (person, score, races, (lower, upper)))

    for pool, score_list in tops.items():
        print('  {:<15}'.format(pool))
        for (p, s, r, b) in score_list:
            print('  {:<25}  {:>5}  /{:>3} = {:>4}{:>15}'
                  .format(p, str(int(s)), str(r), round((s / r), 1), str(b)))
            if score_list.index((p, s, r, b)) == 3:
                break
        print()


def run():
    build_rois()
    # run_raw_performance()
    run_optimized_performance()


run()
