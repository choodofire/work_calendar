import sqlite3
import traceback
import os


DB_NAME = os.getenv("DB_NAME")


def validate_service_address():
    assert DB_NAME is not None, "env variable DB_NAME not set"


def clear_all_tables(db_name):
    connection = None

    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # Clear all tables
        for table in tables:
            table_name = table[0]
            print("Clearing - " + table_name)
            cursor.execute("DELETE FROM %s" % table_name)

        connection.commit()
        print("Successful clearing")

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
    clear_all_tables(db_name)


if __name__ == "__main__":
    main()
