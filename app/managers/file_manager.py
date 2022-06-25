import os
import re

import pandas as pd
from pandas import DataFrame


# def get_files_paths(source_dir_name: str) -> list[str]:
#     files = os.listdir(source_dir_name)
#     paths = []
#     for file in files:
#         paths.append(source_dir_name + "/" + file)
#     return paths

def get_name_from_path(dir_path):
    return dir_path.split("/")[-1]


def get_dir_from_path(file_path: str) -> str:
    return file_path.split("/")[-2]


def read_excel_files(paths: list[str]) -> list[DataFrame]:
    dataframes = []
    for path in paths:
        df = pd.read_excel(path, usecols="A:E")
        dataframes.append(df)
    return dataframes

def read_excel_files_from_source_dir(source_dir_path: str) -> list[str]:
    paths = []
    for directory in get_files_paths(source_dir_path):
        paths.extend(get_files_paths(directory))
    return paths

def get_files_paths(dir_path: str) -> list[str]:
    return [dir_path + "/" + file for file in os.listdir(dir_path)]


def get_date_from_path(path: str, group: int) -> int:
    return int(re.search("(\\d+)-(\\d+)", path).group(group))
