from src.utils.constants import Race


class Storage:
    data: list = []

    @classmethod
    def initialize(cls):
        cls.data = cls.get_dummy_data()

    @classmethod
    def load_from_database(cls):
        # TODO:
        pass

    @classmethod
    def save_to_database(cls):
        # TODO:
        pass

    @classmethod
    def get_race_tuples(cls) -> [(str, int)]:
        return [
            (d[Race.RACE_DATE], d[Race.RACE_NUM]) for d in cls.data
        ]

    @classmethod
    def get_race_tips(cls, race_date: str, race_num: int) -> list:
        matches = list(filter(
            lambda d: d[Race.RACE_DATE] == race_date and d[Race.RACE_NUM] == race_num,
            cls.data
        ))
        if len(matches) == 1:
            return matches[0][Race.TIPS]

    @classmethod
    def get_dummy_data(cls) -> list:
        return [
            {
                'race_date': '2000-01-01',
                'race_num': 1,
                'tips': [],
            },
            {
                'race_date': '2000-01-01',
                'race_num': 2,
                'tips': [],
            },
            {
                'race_date': '2000-01-02',
                'race_num': 1,
                'tips': [],
            },
        ]
