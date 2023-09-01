# work_calendar

Service that provides preconfigured work calendar with http transport. 

## Dev scripts

```bash
# run SQLite 
$ sh dev/run_sqlite_interactive.sh

# create tables ib BD
$ C_TABLE=Calendars D_TABLE=Dates DB_NAME=calendar python dev/create_tables.py

# clear datas in tables
$ DB_NAME=calendar python dev/clear_tables.py

# init new calendar example
$ C_TABLE=Calendars D_TABLE=Dates DB_NAME=calendar TITLE=RU KEY=100 YEAR=2023 python3 dev/create_tables.py
```

## Running app

```bash
$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r requirements.txt

$ gunicorn -b 127.0.0.1:5001 src.wsgi:app

$ gunicorn -b <HOST>:<PORT> src.wsgi:app
```

# Http API

Dates are stored in "YYYYYY-mm-dd" format

Response code 400 and 500 return { 'error': str, 'message': str }

The date, start_date, end_date will be submitted in format "2023-01-01"

| Method | Route             | Body                                        | Response 200                     | Description                                     |
|--------|-------------------|---------------------------------------------|----------------------------------|-------------------------------------------------|
| POST   | /calendar/create  | title:str<br/>key:int                       | {<br/>'key':int<br/>}<br/>       | Create calendar                                 |
| DELETE | /calendar/delete  | key:int                                     | {<br/>'key':int<br/>}            | Delete calendar with dates                      |
| POST   | /holiday/set      | date:str/List[str]<br/>key:int              | {<br/>'dates':List[str]<br/>}    | Set dates as holiday                            |
| POST   | /holiday/unset    | date:str/List[str]<br/>key:int              | {<br/>'dates':List[str]<br/>}    | Unset dates as holiday                          |
| GET    | /holiday/get      | date:str<br/>key:int                        | {<br/>'holiday':Boolean<br/>}    | Get is holiday date                             |
| GET    | /workdays/between | start_date:str<br/>end_date:str<br/>key:int | {<br/>'workdays':int<br/>}       | Get number of working days between dates        |
| GET    | /workdays/month   | month:int<br/>key:int                       | {<br/>'workdays':List[int]<br/>} | Get list of working days in month               |

