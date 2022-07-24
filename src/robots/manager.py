import time
from datetime import date

from src.robots.api import APIRobot
from src.robots.pool import PoolRobot
from src.robots.win_place import WinPlaceOddsRobot
from src.robots.quinella import QuinellaOddsRobot
from src.robots.quinella_place import QuinellaPlaceOddsRobot
from src.robots.forecast import ForecastOddsRobot
from src.storage.storage import Storage
from src.utils.constants import Time, Race
from src.utils.general import \
    get_thread_name, get_current_date_and_time


class RobotManager:
    keep_working = False

    robots: [APIRobot] = [
        PoolRobot(),
        WinPlaceOddsRobot(),
        QuinellaOddsRobot(),
        QuinellaPlaceOddsRobot(),
        ForecastOddsRobot(),
    ]

    @classmethod
    def can_work_on(cls, race_date_to_check: str) -> bool:
        race_date = date.fromisoformat(race_date_to_check)
        next_date = race_date + Time.ONE_DAY
        pre_selling_date = race_date - Time.ONE_DAY
        curr_date, curr_time = get_current_date_and_time()

        if (curr_date == race_date) or \
            (curr_date == pre_selling_date and curr_time >= Time.ONE_PM) or \
            (curr_date == next_date and curr_time <= Time.SIX_AM):
            return True

        return False

    @classmethod
    def stop(cls):
        cls.keep_working = False

    @classmethod
    def work(cls, race_date_to_work: str):
        cls.keep_working = True
        print(f'{get_thread_name()} STARTED')

        races = []
        for (race_date, race_num) in Storage.get_race_tuples():
            if race_date == race_date_to_work:
                race = Storage.get_race(race_date, race_num)
                if race and race not in races:
                    races.append(race)

        while cls.keep_working:
            for race in races:
                race_date, race_num, venue_code = \
                    race[Race.RACE_DATE], race[Race.RACE_NUM], race[Race.VENUE]

                for robot in cls.robots:
                    robot.run(race_date, str(race_num), venue_code)

            Storage.write(race_date_to_work)
            time.sleep(Time.ODDS_FREQUENCY_SEC)

        print(f'{get_thread_name()} ENDED')
