import pandas as pd
from pandas import DataFrame

from app.consts import WIND_TABLE, INT, WIND_DIRECTION_ID, ID, NAME
from app.managers.database_manager import get_dataframe_from_table

wind_dataframe = get_dataframe_from_table(WIND_TABLE)
wind_directions_dictionary = tuple(zip(wind_dataframe[ID], wind_dataframe[NAME], wind_dataframe["name_rus"]))


def parse_wind_direction(wind_direction: int | str, to: int = INT) -> str | int | None:
    if pd.isna(wind_direction):
        return None
    for row in wind_directions_dictionary:
        if wind_direction in row:
            return row[to]
    return None


def translate_wind_direction(dataframe: DataFrame, lang: int):
    for i in range(1, len(dataframe[WIND_DIRECTION_ID]) + 1):
        dataframe[WIND_DIRECTION_ID][i] = parse_wind_direction(dataframe[WIND_DIRECTION_ID][i], lang)
    return dataframe
