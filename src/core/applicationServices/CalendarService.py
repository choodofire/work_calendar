from src.core.domainServices.AbstractCalendarRepository import AbstractCalendarRepository
from typing import Union, List
from datetime import timedelta, datetime
import calendar
import os
import json


class CalendarService:
    def __init__(self, calendar_repository: AbstractCalendarRepository):
        self.calendar_repository = calendar_repository

    def get_calendar_title(self, key: int) -> Union[str, None]:
        return self.calendar_repository.get_calendar_title(key)

    def create_calendar(self, key: int, title: str) -> int:
        calendar_old = self.get_calendar_title(key)
        if calendar_old is not None:
            raise ValueError("Calendar with this key already exists")

        return self.calendar_repository.create_calendar(key, title)

    def delete_calendar(self, key: int) -> int:
        calendar_old = self.get_calendar_title(key)
        if calendar_old is None:
            raise ValueError("Calendar with this key does not exists")

        return self.calendar_repository.delete_calendar(key)

    def set_holiday_in_dates(self, key: int, dates: Union[str, List[str]]) -> List[str]:
        # str in Array
        if isinstance(dates, str):
            dates = [dates]

        calendar_old = self.get_calendar_title(key)
        if calendar_old is None:
            raise ValueError("Calendar with this key does not exists")

        return self.calendar_repository.set_dates_as_holiday(key, dates)

    def unset_holiday_in_dates(self, key: int, dates: Union[str, List[str]]) -> List[str]:
        # str in Array
        if isinstance(dates, str):
            dates = [dates]

        calendar_old = self.get_calendar_title(key)
        if calendar_old is None:
            raise ValueError("Calendar with this key does not exists")

        return self.calendar_repository.unset_dates_as_holiday(key, dates)

    def get_flag_of_date(self, key: int, date: str) -> bool:
        calendar_old = self.get_calendar_title(key)
        if calendar_old is None:
            raise ValueError("Calendar with this key does not exists")

        flag = self.calendar_repository.get_flag_of_date(key, date)
        if flag:
            return True
        else:
            return False

    def count_working_days_in_period(self, key: int, start_date: datetime, end_date: datetime) -> int:
        calendar_old = self.get_calendar_title(key)
        if calendar_old is None:
            raise ValueError("Calendar with this key does not exists")

        # Calculate total number of days in range
        total_days = (end_date - start_date).days + 1

        holidays = self.calendar_repository.get_all_holidays_in_range(key, start_date, end_date)

        # Calculation of number of working days
        working_days = total_days - len(holidays)
        return working_days

    def get_working_days_in_month(self, key: int, month: int) -> List[int]:
        calendar_old = self.get_calendar_title(key)
        if calendar_old is None:
            raise ValueError("Calendar with this key does not exists")

        holidays_in_month = self.calendar_repository.get_all_holidays_in_month(key, month)

        # get the current year
        current_year = int(holidays_in_month[0].split('-')[0])

        working_day_numbers = []
        # Get number of days in given month
        _, num_days = calendar.monthrange(current_year, month)
        # Going through all days of month
        for day in range(1, num_days + 1):
            # Form line with date in format "YYYYY-MM-DD"
            date_str = datetime(current_year, month, day).strftime("%Y-%m-%d")
            # Check if current date is holiday
            if date_str not in holidays_in_month:
                working_day_numbers.append(day)

        return working_day_numbers
