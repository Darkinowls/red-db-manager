from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from pandas import DataFrame

from app.consts import NO_DATA_IN_THE_TABLE, ERROR, NO_DATE_GAPS_FOUND, LOCATED_IN_THE_TABLE, INFORMATION, SUCCESS, \
    WIND_DIRECTION_ID, WARNING, METHODS, WIND_SPEED, TEMPERATURE, APPEND, REPLACE, UA, WEATHER_TABLE
from app.formatters.message_formatter import data_gaps_located_message, rows_were_affected_message
from app.formatters.wind_direction_formatter import translate_wind_direction
from app.gui.PandasModel import PandasModel
from app.gui.UiTab1 import UiTab1
from app.managers.database_manager import is_database_table_empty, save_database_table
from app.managers.dataframe_manager import get_weather_api, check_for_filling_needed, locate_datetime_gaps, \
    fill_gaps_by_interpolation, fill_gaps_by_pad, split_datetime
from app.managers.file_manager import read_excel_files
from app.windows.QMessanger import QMessanger


class Tab1(UiTab1):
    __filenames: list[str]
    __weather_api: DataFrame = None
    __marked_weather_api: DataFrame | None
    __messanger: QMessanger
    __need_padding: bool
    __no_date_gaps: bool
    __gap_info: list[tuple[datetime, datetime]] | None

    def setupUi(self, main_window):
        UiTab1.setupUi(self, main_window)
        self.__messanger = QMessanger()
        self.button_import_files.clicked.connect(self.__import_excel_files)
        self.button_locate_gaps.clicked.connect(self.__locate_gaps)
        self.button_safe_db.clicked.connect(self.__safe_to_database)
        self.button_fill_gaps.clicked.connect(self.__fill_gaps)
        self.button_export_files.clicked.connect(self.__export_files)

    def __import_excel_files(self):
        options = QFileDialog.Options()
        self.__filenames, _ = QFileDialog.getOpenFileNames(None, "Open excel files", "",
                                                           "Excel Files (*.xlsx)", options=options, )
        if not self.__filenames:
            return
        self.__weather_api = get_weather_api(read_excel_files(self.__filenames), self.__filenames)
        self.tableView.setModel(PandasModel(self.__weather_api))
        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 125)
        self.tableView.setColumnWidth(2, 150)
        self.tableView.setColumnWidth(3, 125)
        self.__need_padding = check_for_filling_needed(self.__weather_api, WIND_DIRECTION_ID)
        self.__marked_weather_api = None
        self.__no_date_gaps = False
        self.__gap_info = None

    def __locate_gaps(self) -> int:
        if self.tableView.model() is None:
            return self.__messanger.show_message(NO_DATA_IN_THE_TABLE, ERROR, QMessageBox.Critical)
        if self.__no_date_gaps:
            return self.__messanger.show_message(NO_DATE_GAPS_FOUND, INFORMATION, QMessageBox.Information)
        if self.__gap_info is not None:
            return self.__messanger.show_message(LOCATED_IN_THE_TABLE, INFORMATION, QMessageBox.Information)
        weather_marked, self.__gap_info = locate_datetime_gaps(self.__weather_api)
        if self.__gap_info:
            self.__weather_api = weather_marked
            self.__need_padding = True
            self.tableView.setModel(PandasModel(self.__weather_api))
            message = data_gaps_located_message(self.__gap_info)
            return self.__messanger.show_message(message, SUCCESS, QMessageBox.Information)
        self.__no_date_gaps = True
        return self.__messanger.show_message(NO_DATE_GAPS_FOUND, INFORMATION, QMessageBox.Information)

    def __fill_gaps(self) -> int:
        if self.tableView.model() is None:
            return self.__messanger.show_message(NO_DATA_IN_THE_TABLE, ERROR, QMessageBox.Critical)
        self.__do_padding()
        self.__do_interpolation()

    def __do_padding(self):
        if self.__need_padding and self.__messanger.question_message_padding_data():
            self.__weather_api = fill_gaps_by_pad(self.__weather_api, [WIND_DIRECTION_ID])
            self.tableView.setModel(PandasModel(self.__weather_api))
            self.__need_padding = False

    def __do_interpolation(self) -> int:
        if self.__gap_info is None:
            return self.__messanger.show_message('Date gaps are not located in the table', WARNING, QMessageBox.Warning)
        answer = self.__messanger.question_message_fill_method()
        if answer != QMessageBox.Ignore:
            if self.__marked_weather_api is None:
                self.__marked_weather_api = self.__weather_api.__copy__()
            self.__weather_api = fill_gaps_by_interpolation(self.__marked_weather_api.__copy__(),
                                                            METHODS.get(answer),
                                                            [WIND_SPEED, TEMPERATURE])
            self.tableView.setModel(PandasModel(self.__weather_api))
        return answer

    def __safe_to_database(self) -> int:
        if self.tableView.model() is None:
            return self.__messanger.show_message(NO_DATA_IN_THE_TABLE, ERROR, QMessageBox.Critical)
        if not is_database_table_empty(WEATHER_TABLE):
            response = self.__messanger.question_message_erase_data()
            if response == QMessageBox.Cancel:
                return QMessageBox.Cancel
        else:
            response: int = QMessageBox.No
        affected: int = save_database_table(self.__weather_api, WEATHER_TABLE,
                                            APPEND if response == QMessageBox.No
                                            else REPLACE)
        message = rows_were_affected_message(affected)
        return self.__messanger.show_message(message, SUCCESS, QMessageBox.Information)

    def __export_files(self) -> int:
        if self.tableView.model() is None:
            return self.__messanger.show_message(NO_DATA_IN_THE_TABLE, ERROR, QMessageBox.Critical)
        translate_wind_direction(split_datetime(self.__weather_api.__copy__()), lang=UA).to_excel("output.xlsx")
        return self.__messanger.show_message('Data have been exported', SUCCESS, QMessageBox.Information)
