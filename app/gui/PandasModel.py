from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from pandas import DataFrame

from app.consts import UA
from app.formatters.wind_direction_formatter import translate_wind_direction


class PandasModel(QtCore.QAbstractTableModel):
    __data: DataFrame = None
    __columns = ['data and time', 'temperature', 'wind direction', 'wind speed']

    def __init__(self, data: DataFrame, lang: int = UA, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__data = translate_wind_direction(data.__copy__(), lang)

    def rowCount(self, parent=None) -> int:
        return len(self.__data.values)

    def columnCount(self, parent=None) -> int:
        return self.__data.columns.size

    def data(self, index, role=Qt.DisplayRole) -> str | None:
        if index.isValid() and role == Qt.DisplayRole:
            return str(self.__data.iloc[index.row()][index.column()])
        return None

    def headerData(self, p_int: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.__columns[p_int])

            if orientation == Qt.Vertical:
                return str(self.__data.index[p_int])
        return None
