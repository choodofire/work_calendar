import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
from src.core.domainServices.AbstractCalendarRepository import AbstractCalendarRepository
from typing import List, Union

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_CALENDARS_TABLE_NAME = os.getenv("DB_CALENDARS_TABLE_NAME")
DB_DATES_TABLE_NAME = os.getenv("DB_DATES_TABLE_NAME")


class SqliteRepository(AbstractCalendarRepository):
    def __init__(self):
        self._db_name = DB_NAME + ".db"
        self._connection = None

    @property
    def db_name(self):
        return self._db_name

    def _connect(self) -> None:
        try:
            self._connection = sqlite3.connect(self._db_name)
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def _connect_get_cursor(self) -> sqlite3.Connection.cursor:
        self._connection = sqlite3.connect(self._db_name)
        return self._connection.cursor()

    def create_calendar(self, key: int, title: str) -> int:
        cursor = self._connect_get_cursor()

        # Inserting calendar into Calendars Table with parameterized query
        cursor.execute(f"""
                        INSERT INTO {DB_CALENDARS_TABLE_NAME} (title, key)
                        VALUES (?, ?)
                        """, (title, key))

        self._connection.commit()
        self._connection.close()
        return key

    def delete_calendar(self, key: int) -> int:
        cursor = self._connect_get_cursor()

        # Deleting rows from "Dates" table where calendar_key = key
        cursor.execute(f"""
                            DELETE FROM {DB_DATES_TABLE_NAME}
                            WHERE calendar_key = ?
                            """, (key,))

        # Deleting row from "Calendars" table with key
        cursor.execute(f"""
                            DELETE FROM {DB_CALENDARS_TABLE_NAME}
                            WHERE key = ?
                            """, (key,))

        self._connection.commit()
        self._connection.close()
        return key

    def set_dates_as_holiday(self, key: int, dates: List[str]) -> List[str]:
        cursor = self._connect_get_cursor()

        result = []
        # insert every date
        for date in dates:
            cursor.execute(f"""
                        INSERT INTO {DB_DATES_TABLE_NAME} (date, flag, calendar_key)
                        VALUES (?, 1, ?)
                        """, (date, key))
            result.append(date)

        self._connection.commit()
        self._connection.close()
        return result

    def unset_dates_as_holiday(self, key: int, dates: List[str]) -> List[str]:
        cursor = self._connect_get_cursor()

        result = []
        # delete every date
        for date in dates:
            cursor.execute(f"""
                        DELETE FROM {DB_DATES_TABLE_NAME}
                        WHERE date = ? AND calendar_key = ?
                        """, (date, key))
            result.append(date)

        self._connection.commit()
        self._connection.close()
        return result

    def get_calendar_title(self, key: int) -> Union[str, None]:
        cursor = self._connect_get_cursor()

        # Get title from "CalendarTable" table where key = given key
        cursor.execute(f"SELECT title FROM {DB_CALENDARS_TABLE_NAME} WHERE key = '{key}'")
        calendar = cursor.fetchone()

        self._connection.close()

        if calendar:
            return calendar[0]
        else:
            return None

    def get_flag_of_date(self, key: int, date: str) -> bool:
        cursor = self._connect_get_cursor()

        # Get flag from "Dates" table where calendar_id = given key and date = given date
        cursor.execute(f"SELECT flag FROM {DB_DATES_TABLE_NAME} WHERE calendar_key = '{key}' AND date = '{date}'")
        result = cursor.fetchone()

        self._connection.close()

        if result:
            return True
        else:
            return False

    def get_all_holidays(self, key: int) -> List[datetime]:
        cursor = self._connect_get_cursor()

        query = f"SELECT date FROM {DB_DATES_TABLE_NAME} WHERE calendar_key = ? AND flag = 1"
        cursor.execute(query, (key,))
        rows = cursor.fetchall()

        holidays = []
        for row in rows:
            date_str = row[0]  # Get string with date from query result
            date_only = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert string to datetime object
            holidays.append(date_only)

        self._connection.close()
        return holidays

    def get_all_holidays_in_range(self, key: int, start_date: datetime, end_date: datetime) -> List[datetime]:
        cursor = self._connect_get_cursor()

        query = f"SELECT date FROM {DB_DATES_TABLE_NAME} WHERE calendar_key = ? AND flag = 1 AND date BETWEEN ? AND ?"
        cursor.execute(query, (key, start_date, end_date))
        rows = cursor.fetchall()

        holidays = []
        for row in rows:
            date_str = row[0]  # Get string with date from query result
            date_only = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert string to datetime object
            holidays.append(date_only)

        self._connection.close()
        return holidays

    def get_all_holidays_in_month(self, key: int, month: int) -> List[str]:
        cursor = self._connect_get_cursor()

        formatted_month = str(month).zfill(2)

        query = f"SELECT date FROM {DB_DATES_TABLE_NAME} " \
                f"WHERE calendar_key = ? AND strftime('%m', date) = ? AND flag = 1"
        cursor.execute(query, (key, formatted_month))
        holidays = [row[0] for row in cursor.fetchall()]

        self._connection.close()
        return holidays
