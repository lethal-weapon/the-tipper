class CypherConverter:

    @classmethod
    def add_quote(cls, text: str):
        return '\'{}\''.format(text)

    @classmethod
    def to_date(cls, text: str):
        # e.g. '2021-12-09'
        return 'date({})'.format(cls.add_quote(text))
