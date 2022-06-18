import os
import re

import pandas as pd
from pandas import DataFrame


def get_files_paths(source_dir_name: str) -> list[str]:
    files = os.listdir(source_dir_name)
    paths = []
    for file in files:
        paths.append(source_dir_name + "/" + file)
    return paths


def read_excel_files(paths: list[str]) -> list[DataFrame]:
    dataframes = []
    for path in paths:
        df = pd.read_excel(path, usecols="A:E")
        dataframes.append(df)
    return dataframes


def get_date_from_path(path: str, group: int) -> int:
    return int(re.search("(\\d+)-(\\d+)", path).group(group))
