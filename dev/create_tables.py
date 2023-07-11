import sqlite3
import traceback
import os


CALENDARS_TABLE = os.getenv("C_TABLE")
DATES_TABLE = os.getenv("D_TABLE")
DB_NAME = os.getenv("DB_NAME")


def validate_service_address():
    assert CALENDARS_TABLE is not None, "env variable C_TABLE not set"
    assert DATES_TABLE is not None, "env variable D_TABLE not set"
    assert DB_NAME is not None, "env variable DB_NAME not set"


def create_all_tables(db_name):
    connection = None

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Creating table "Calendars"
        cursor.execute("CREATE TABLE IF NOT EXISTS " + CALENDARS_TABLE + " ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                title TEXT, \
                key INTEGER UNIQUE \
            )")

        # Creating table "Holidays" with Foreign Key on "Calendars"
        cursor.execute("CREATE TABLE IF NOT EXISTS " + DATES_TABLE + " ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                date DATE, \
                flag INTEGER CHECK (flag IN (0, 1)), \
                calendar_key INTEGER, \
                FOREIGN KEY (calendar_key) REFERENCES " + CALENDARS_TABLE + " (key) \
            )")

        connection.commit()
        print("Successful creation")

    except Exception as e:
        # Error print
        print("Error in table clearing: %s" % e)
        traceback.print_exc()
    finally:
        if connection:
            connection.close()


def main():
    validate_service_address()
    db_name = DB_NAME + ".db"
    create_all_tables(db_name)


if __name__ == "__main__":
    main()

