import datetime
import warnings
from datetime import timedelta, datetime

import numpy as np
import pandas as pd
from pandas import DataFrame

from app.consts import DATETIME, EXCEL_DAY, UTC, EXCEL_WIND_DIRECTION, TIME_GAP, T, EXCEL_FF, TEMPERATURE, \
    WIND_DIRECTION_ID, WIND_SPEED, PAD, DATE, TIME
from app.formatters.wind_direction_formatter import parse_wind_direction
from app.managers.file_manager import get_date_from_path


def locate_datetime_gaps(dataframe: DataFrame) -> tuple[DataFrame, list[tuple[datetime, datetime]]]:
    gap_info = []
    for i in range(len(dataframe[DATETIME]) - 1):
        if dataframe[DATETIME][i + 2] - dataframe[DATETIME][i + 1] != timedelta(days=0, minutes=30):
            gap_info.append((dataframe[DATETIME][i + 1], dataframe[DATETIME][i + 2]))
            dataframe, num_rows = insert_into_dataframe_datetime_rows(dataframe, i, TIME_GAP)
            i += num_rows
    return dataframe, gap_info


def insert_into_dataframe_datetime_rows(dataframe: DataFrame, row: int, time_gap: str) -> tuple[DataFrame, int]:
    date_times = pd.date_range(start=dataframe[DATETIME][row + 1], end=dataframe[DATETIME][row + 2], freq=time_gap,
                               inclusive='neither')
    columns = dataframe.columns
    for i in range(len(date_times)):
        dataframe = pd.DataFrame(
            np.insert(dataframe.values, row + 1 + i, values=[date_times[i], None, None, None], axis=0))
    dataframe.columns = columns
    dataframe.index += 1
    return dataframe, len(date_times)


def get_weather_api(dataframes: list[DataFrame], paths: list[str]) -> DataFrame:
    weathers_api = []
    for i in range(len(dataframes)):
        weathers_api.append(
            create_weather_dataframe(dataframes[i], get_date_from_path(paths[i], 2), get_date_from_path(paths[i], 1))
        )
    return merge_sort_dataframe_list(weathers_api, DATETIME)


def create_weather_dataframe(dataframe: DataFrame, month: int, year: int) -> DataFrame:
    rows = []
    for i in range(len(dataframe.index)):
        try:
            rows.append([
                datetime.combine(datetime(year, month, dataframe.at[i, EXCEL_DAY]), dataframe.at[i, UTC]),
                dataframe.at[i, T],
                parse_wind_direction(dataframe.at[i, EXCEL_WIND_DIRECTION]),
                dataframe.at[i, EXCEL_FF]
            ])
        except ValueError as warning:
            warnings.warn(warning.args[0])

    database_dataframe = pd.DataFrame(rows, columns=[DATETIME, TEMPERATURE, WIND_DIRECTION_ID,
                                                     WIND_SPEED])
    return database_dataframe


def merge_sort_dataframe_list(dataframes: list[DataFrame], sort_by: str):
    dataframe = pd.concat(dataframes, ignore_index=True)
    dataframe = dataframe.sort_values(by=sort_by)
    dataframe = dataframe.reset_index(drop=True)
    dataframe.index += 1
    return dataframe


def fill_gaps_by_interpolation(dataframe: DataFrame, f_method: str, columns: list[str]) -> DataFrame:
    for column in columns:
        dataframe[column] = dataframe[column].astype(float).interpolate(method=f_method, order=3).round(0).astype(int)
    return dataframe


def fill_gaps_by_pad(dataframe: DataFrame, pad_columns: list[str]) -> DataFrame:
    for pad_column in pad_columns:
        dataframe[pad_column] = dataframe[pad_column].astype(float).interpolate(method=PAD).round(0).astype(int)
    return dataframe


def check_for_filling_needed(dataframe: DataFrame, column: str) -> bool:
    if dataframe[column].isnull().values.any():
        return True
    return False


def split_datetime(dataframe: DataFrame) -> DataFrame:
    dataframe.insert(0, DATE, dataframe[DATETIME].dt.date)
    dataframe.insert(1, TIME, dataframe[DATETIME].dt.time)
    del dataframe[DATETIME]
    return dataframe
