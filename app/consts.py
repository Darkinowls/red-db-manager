import os

from dotenv import load_dotenv

ID = 'id'
NAME = 'name'
APPEND = 'append'
REPLACE = 'replace'
PAD = 'pad'
TIME_GAP = '30T'
EXCEL_FF = 'FF'
WIND_SPEED = 'wind_speed'
WIND_DIRECTION_ID = 'wind_direction_id'
TEMPERATURE = 'temperature'
T = 'T'
S = 'T'
UTC = 'UTC'
DATETIME = 'datetime'
EXCEL_WIND_DIRECTION = 'dd'
EXCEL_DAY = 'Число месяца'
DATETIME_FORMAT = '%Y.%m.%d %H:%M'
INT = 0
UA = 1
RUS = 2
ANGLE = 3
WIND_TABLE = "wind_directions"
WARNING = 'Warning'
NO_DATE_GAPS_FOUND = "No date gaps found"
LOCATED_IN_THE_TABLE = 'All the date gaps are located in the table'
INFORMATION = "Information"
SUCCESS = "Success"
ERROR = "Error"
NO_DATA_IN_THE_TABLE = "There is no data in the table"
METHODS: dict[int, str] = dict({0: 'spline', 1: 'linear', 2: 'polynomial'})
DATE = 'date'
TIME = 'time'
RED_ROSE = "Red Rose"
REGION = 'region'
load_dotenv()
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
USER = os.getenv('TEMP_USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
WEATHER_TABLE = os.getenv('WEATHER_TABLE')
CHARSET = os.getenv('CHARSET')
CODE = os.getenv('CODE')
KEY = int(os.getenv('KEY'))
ACTIVATED = bool(os.getenv('ACTIVATED'))
NAG_TIME = 1000 * 60 * 5
CAPTCHA = "captcha"
