import time
from datetime import datetime, date

from src.robots.api import APIRobot
from src.robots.pool import PoolRobot
from src.robots.win_place import WinPlaceOddsRobot
from src.robots.quinella import QuinellaOddsRobot
from src.robots.quinella_place import QuinellaPlaceOddsRobot
from src.robots.forecast import ForecastOddsRobot
from src.storage.storage import Storage
from src.utils.constants import Time, Race
from src.utils.general import \
    get_thread_name, get_now, get_current_date_and_time


class RobotManager:
    keep_working: False

    robots: [APIRobot] = [
        PoolRobot(),
        WinPlaceOddsRobot(),
        QuinellaOddsRobot(),
        QuinellaPlaceOddsRobot(),
        ForecastOddsRobot(),
    ]

    @classmethod
    def has_pool_opened(cls, race_date_to_check: str):
        race_date = date.fromisoformat(race_date_to_check)
        bet_date = race_date - Time.ONE_DAY
        curr_date, curr_time = get_current_date_and_time()

        if (curr_date >= race_date) or \
            (curr_date >= bet_date and curr_time >= Time.ONE_PM):
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
                race_date, race_num, race_time, venue_code = \
                    race[Race.RACE_DATE], race[Race.RACE_NUM], \
                    race[Race.TIME], race[Race.VENUE]

                now = get_now()
                begin_time = datetime.fromisoformat(race_time)

                # no need to make the call if too early or too late
                if (begin_time - now > Time.TWO_HOURS) or \
                    (now - begin_time > Time.ONE_HOUR):
                    continue

                for robot in cls.robots:
                    robot.run(race_date, str(race_num), venue_code)

            Storage.write(race_date_to_work)
            time.sleep(Time.ODDS_FREQUENCY)

        print(f'{get_thread_name()} ENDED')
