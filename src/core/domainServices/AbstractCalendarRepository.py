from abc import ABC, abstractmethod
from typing import List, Union
from datetime import datetime


class AbstractCalendarRepository(ABC):
    @abstractmethod
    def create_calendar(self, key: int, title: str) -> int:
        pass

    @abstractmethod
    def delete_calendar(self, key: int) -> int:
        pass

    @abstractmethod
    def set_dates_as_holiday(self, key: int, dates: List[str]) -> List[str]:
        pass

    @abstractmethod
    def unset_dates_as_holiday(self, key: int, dates: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_calendar_title(self, key: int) -> Union[str, None]:
        pass

    @abstractmethod
    def get_flag_of_date(self, key: int, date: str) -> bool:
        pass

    @abstractmethod
    def get_all_holidays(self, key: int) -> List[datetime]:
        pass

    @abstractmethod
    def get_all_holidays_in_range(self, key: int, start_date: datetime, end_date: datetime) -> List[datetime]:
        pass

    @abstractmethod
    def get_all_holidays_in_month(self, key: int, month: int) -> List[str]:
        pass
