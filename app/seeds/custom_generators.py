from flask_seeder import generator
from datetime import datetime, timezone, timedelta
import random

name_list_path = "./app/seeds/data/names/names.txt"


def read_txt_file_with_names_line_by_line(path):
    with open(path) as name:
        return name.read().splitlines()


class SequenceList(generator.Sequence):
    def __init__(self, list: list):
        super().__init__(start=0, end=len(list))
        self._list = list

    def generate(self):
        value = self._next
        self._next += 1

        return self._list[value]


class CustomNameGenerator(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        if self._lines is None:
            self._lines = read_txt_file_with_names_line_by_line(
                name_list_path)

        result = self.rnd.choice(self._lines)

        return result


class DateGenerator(generator.Generator):

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(**kwargs)
        self._start_date = start_date

    def generate(self):
        days_to_generate_dates = timedelta(days=8)
        end_date = datetime.now(timezone.utc)
        random_date = self._start_date + \
            random.randrange((end_date - self._start_date) //
                             days_to_generate_dates + 1) * days_to_generate_dates

        return random_date
