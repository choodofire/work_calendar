import traceback
from typing import List
from datetime import datetime
from flask import Blueprint, request, jsonify
from src.core.applicationServices.CalendarService import CalendarService
from src.infrastructure.db.SqliteRepository import SqliteRepository

calendar_API = Blueprint('calendar', __name__)
service = CalendarService(SqliteRepository())


@calendar_API.route('/calendar/create', methods=['POST'])
def create_calendar():
    try:
        data = request.get_json()
        title = data['title']
        key = data['key']
        if not title or not isinstance(key, int) or key <= 0:
            raise ValueError()

        result = service.create_calendar(key, title)
        if result:
            return jsonify({'key': result}), 200
        else:
            raise ValueError("Get error in calendar creating")

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@calendar_API.route('/calendar/delete', methods=['DELETE'])
def delete_calendar():
    try:
        data = request.get_json()
        key = data['key']
        if not isinstance(key, int) or key <= 0:
            raise ValueError()

        result = service.delete_calendar(key)
        if result:
            return jsonify({'key': result}), 200
        else:
            raise ValueError("Get error in calendar deleting")

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@calendar_API.route('/holiday/set', methods=['POST'])
def set_holiday():
    try:
        data = request.get_json()
        date = data['date']
        key = data['key']
        # Check that date is str or List[str] and key is int > 0
        if not date or \
                not (isinstance(date, str) or (isinstance(date, List) and all(isinstance(item, str) for item in date)))\
                or not isinstance(key, int) or key <= 0:
            raise ValueError()

        result = service.set_holiday_in_dates(key, date)
        return jsonify({'dates': result}), 200

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@calendar_API.route('/holiday/unset', methods=['POST'])
def unset_holiday():
    try:
        data = request.get_json()
        date = data['date']
        key = data['key']
        # Check that date is str or List[str] and key is int > 0
        if not date or \
                not (isinstance(date, str) or (isinstance(date, List) and all(isinstance(item, str) for item in date)))\
                or not isinstance(key, int) or key <= 0:
            raise ValueError()

        result = service.unset_holiday_in_dates(key, date)
        return jsonify({'dates': result}), 200

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@calendar_API.route('/holiday/get', methods=['GET'])
def get_holiday():
    try:
        data = request.get_json()
        date = data['date']
        key = data['key']
        if not isinstance(date, str) or not isinstance(key, int) or key <= 0:
            raise ValueError()

        result = service.get_flag_of_date(key, date)
        return jsonify({'holiday': result}), 200

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@calendar_API.route('/workdays/between', methods=['GET'])
def get_workdays_between():
    try:
        data = request.get_json()
        start_date = data['start_date']
        end_date = data['end_date']
        key = data['key']
        if not isinstance(start_date, str) or not isinstance(end_date, str) or not isinstance(key, int) or key <= 0:
            raise ValueError()

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        result = service.count_working_days_in_period(key, start_date, end_date)
        return jsonify({'workdays': result}), 200

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500


@calendar_API.route('/workdays/month', methods=['GET'])
def get_workdays_in_month():
    try:
        data = request.get_json()
        month = data['month']
        key = data['key']
        if not isinstance(month, int) or month <= 0 or month > 12 or not isinstance(key, int) or key <= 0:
            raise ValueError()

        result = service.get_working_days_in_month(key, month)
        return jsonify({'workdays': result}), 200

    except ValueError as ve:
        return jsonify({'error': 'Invalid data format', 'message': str(ve)}), 400
    except KeyError as ke:
        return jsonify({'error': 'Missing required fields', 'message': str(ke)}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
