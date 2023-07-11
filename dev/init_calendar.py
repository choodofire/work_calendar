import sqlite3
import traceback
import os
import json
from typing import List


CALENDARS_TABLE = os.getenv("C_TABLE")
DATES_TABLE = os.getenv("D_TABLE")
DB_NAME = os.getenv("DB_NAME")
TITLE = os.getenv("TITLE")
KEY = int(os.getenv("KEY"))
YEAR = int(os.getenv("YEAR"))
FILENAME = "holidays.json"


def validate_service_address():
    assert CALENDARS_TABLE is not None, "env variable C_TABLE not set"
    assert DATES_TABLE is not None, "env variable D_TABLE not set"
    assert DB_NAME is not None, "env variable DB_NAME not set"
    assert TITLE is not None, "env variable TITLE not set"
    assert KEY is not None, "env variable KEY not set"
    assert YEAR is not None, "env variable YEAR not set"
    if not isinstance(YEAR, int) or YEAR <= 2000 or not isinstance(KEY, int) or KEY <= 0:
        raise ValueError()


def get_holidays_by_year_from_json(filepath: str, year: int) -> List[str]:
    with open(filepath) as file:
        data = json.load(file)
        holidays = data['holidays']

        holidays_in_year = []
        for holiday in holidays:
            holiday_year = int(holiday.split('-')[0])
            if holiday_year == year:
                holidays_in_year.append(holiday)

        return holidays_in_year


def set_dates_as_holiday(cursor, key: int, dates: List[str]) -> List[str]:
    result = []
    # insert every date
    for date in dates:
        cursor.execute(f"""
                    INSERT INTO {DATES_TABLE} (date, flag, calendar_key)
                    VALUES (?, 1, ?)
                    """, (date, key))
        result.append(date)

    return result


def init_calendar(db_name):
    connection = None

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Get calendar from "Calendar" table where key = given key
        cursor.execute(f"SELECT title FROM {CALENDARS_TABLE} WHERE key = '{KEY}'")
        calendar = cursor.fetchone()
        if calendar:
            raise ValueError("Calendar with this key already exists")

        # Create calendar
        cursor.execute(f"""
                        INSERT INTO {CALENDARS_TABLE} (title, key)
                        VALUES (?, ?)
                        """, (TITLE, KEY))

        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "files", "json", FILENAME))

        # Get holidays from file
        holidays_in_year = get_holidays_by_year_from_json(file_path, YEAR)

        set_dates_as_holiday(cursor, KEY, holidays_in_year)

        connection.commit()
        print("Successful init new calendar")

    except ValueError as ve:
        print({'error': 'Invalid data format', 'message': str(ve)})
    except KeyError as ke:
        print({'error': 'Missing required fields', 'message': str(ke)})
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
    finally:
        if connection:
            connection.close()


def main():
    validate_service_address()
    db_name = DB_NAME + ".db"
    init_calendar(db_name)


if __name__ == "__main__":
    main()
