import json
import os
from pathlib import Path
from typing import Union

import pandas as pd
from pandas import Timestamp
from workalendar.europe import Russia

from dreamml.logging import get_logger

_logger = get_logger(__name__)


class RusProductionCalendar:
    def __init__(self, calendars_path: Union[Path, str]):
        self.calendars_path = calendars_path

        if os.path.exists(self.calendars_path):
            with open(calendars_path, "r") as f:
                self.calendars = json.load(f)
        else:
            raise ValueError(f'Path "{self.calendars_path}" doesn`t exist.')

        self.worcalendar = Russia()
        self.years = []
        for year, _ in self.calendars.items():
            self.years.append(int(year))

    def _check_date_in_calendar(self, row: Timestamp):
        if int(row.year) in self.years:
            return True
        return False

    def check_date_is_holiday(self, row: Timestamp):
        if self._check_date_in_calendar(row):
            calendar_year_month = self.calendars[str(row.year)][str(row.month)]
            if int(row.day) in calendar_year_month["holidays"]:
                return 1
            return 0
        else:
            if self.worcalendar.is_holiday(row):
                return 1
            return 0

    def check_date_is_pre_holiday(self, row: Timestamp):
        if self._check_date_in_calendar(row) is True:
            calendar_year_month = self.calendars[str(row.year)][str(row.month)]
            if int(row.day) in calendar_year_month["pre_holidays"]:
                return 1
            return 0
        else:
            if self.worcalendar.is_working_day(row) and self.worcalendar.is_holiday(
                row + pd.DateOffset(days=1)
            ):
                return 1
            return 0

    def check_date_is_weekend(self, row: Timestamp):
        if self._check_date_in_calendar(row) is True:
            calendar_year_month = self.calendars[str(row.year)][str(row.month)]
            if int(row.day) in calendar_year_month["weekends"]:
                return 1
            return 0
        else:
            if row.day_of_week in [5, 6]:
                return 1
            return 0