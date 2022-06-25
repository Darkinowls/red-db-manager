import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame
from windrose import WindroseAxes

from app.consts import WEATHER_TABLE, UA, ANGLE, WIND_DIRECTION_ID
from app.formatters.wind_direction_formatter import translate_wind_direction
from app.gui.UiTab2 import UiTab2
from app.managers.database_manager import get_dataframe_from_table
from app.windows.QMessanger import QMessanger


class Tab2(UiTab2):
    __dir_path: str
    __filenames: list[str]
    __region: str
    __from_date: datetime
    __to_date: datetime
    __weather_api: DataFrame

    def setupUi(self, main_window):
        UiTab2.setupUi(self, main_window)
        self.calendar_from.setEnabled(False)
        self.calendar_to.setEnabled(False)
        self.button_import_regions.clicked.connect(self.__import_regions)
        self.comboBox.currentIndexChanged.connect(self.__choose_region)
        self.calendar_from.clicked.connect(self.__choose_date_from)
        self.calendar_to.clicked.connect(self.__choose_date_to)
        self.button_duration_temperature.clicked.connect(self.__show_duration_temperature)
        self.button_conditions.clicked.connect(self.__show_conditions_temperature)
        self.button_duration_wind.clicked.connect(self.__show_duration_wind)
        self.button_rose.clicked.connect(self.__show_rose)
        self.button_export_pdf.clicked.connect(self.__export_pdf)

    def __export_pdf(self):
        if not self.calendar_from.isEnabled():
            return QMessanger().show_message('Data is not imported', 'Warning', QMessageBox.Warning)
        self.__get_conditions_temperature()
        self.__get_duration_temperature()
        self.__get_duration_wind()
        self.__get_rose()
        try:
            with PdfPages(
                    'report_' + self.__region + '_from_' + self.__from_date.strftime(
                        '%d.%m.%y') + '_to_' + self.__to_date.strftime
                        ('%d.%m.%y') + '.pdf') as pdf:
                for i in plt.get_fignums():
                    if i in plt.get_fignums()[-4:]:
                        pdf.savefig(plt.figure(i))
                    plt.close(plt.figure(i))
        except Exception as e:
            QMessanger().show_message(str(e), 'Error', QMessageBox.Critical)

    def __show_rose(self):
        if not self.calendar_from.isEnabled():
            return QMessanger().show_message('Data is not imported', 'Warning', QMessageBox.Warning)
        self.__get_rose().show()

    def __get_rose(self):
        try:
            df = self.__get_df()
            df['wind_direction_id'] = translate_wind_direction(df, UA)
            df = df[(df['wind_direction_id'] != 'Змінний') & (df['wind_speed'] > 0)]
            df[WIND_DIRECTION_ID] = translate_wind_direction(df, ANGLE)
            wind_rose: WindroseAxes = WindroseAxes.from_ax()
            bins = df['wind_speed'].unique().tolist()
            bins.sort()
            wind_rose.bar(df[WIND_DIRECTION_ID], df['wind_speed'], bins=bins)
            plt.title('Rose wind')
            wind_rose.set_legend(title='Wind speed')
            return plt
        except Exception as e:
            QMessanger().show_message(str(e), 'Error', QMessageBox.Critical)

    def __show_duration_wind(self):
        if not self.calendar_from.isEnabled():
            return QMessanger().show_message('Data is not imported', 'Warning', QMessageBox.Warning)
        self.__get_duration_wind().show()

    def __get_duration_wind(self):
        df_in_range = self.__get_df()
        df_counted = df_in_range.groupby('wind_speed')['datetime'].count() / 2
        plt.figure()
        df_counted.plot(y='datetime', kind='bar')
        plt.title('Wind regime')
        plt.xlabel("Wind")
        plt.ylabel("Hours")
        return plt

    def __show_conditions_temperature(self):
        if not self.calendar_from.isEnabled():
            return QMessanger().show_message('Data is not imported', 'Warning', QMessageBox.Warning)
        self.__get_conditions_temperature().show()

    def __get_conditions_temperature(self) -> plt:
        df = self.__get_df()
        plt.figure()
        df.plot(x='datetime', y='temperature', kind='line')
        plt.title('Temperature conditions')
        plt.xlabel("Date and time")
        plt.ylabel("Temperature")
        return plt

    def __show_duration_temperature(self):
        if not self.calendar_from.isEnabled():
            return QMessanger().show_message('Data is not imported', 'Warning', QMessageBox.Warning)
        self.__get_duration_temperature().show()

    def __get_duration_temperature(self):
        df_in_range = self.__get_df()
        df_counted = df_in_range.groupby('temperature')['datetime'].count() / 2
        plt.figure()
        df_counted.plot(y='datetime', kind='bar')
        plt.title('Temperature regime')
        plt.xlabel("Temperature")
        plt.ylabel("Hours")
        return plt

    def __get_df(self) -> DataFrame:
        df_by_region = self.__weather_api[self.__weather_api['region'] == self.__region]
        df = df_by_region[(df_by_region['datetime'] >= self.__from_date)
                          & (df_by_region['datetime'] <= self.__to_date)]
        return df

    def __choose_date_from(self) -> int:
        from_date = pd.to_datetime(self.calendar_from.selectedDate().toPyDate())
        if from_date > self.__to_date:
            self.calendar_from.setSelectedDate(self.__from_date)
            return QMessanger().show_message('To date must be greater than from date', 'Warning', QMessageBox.Warning)
        self.__from_date = from_date

    def __choose_date_to(self) -> int:
        to_date = pd.to_datetime(self.calendar_to.selectedDate().toPyDate())
        if self.__from_date > to_date:
            self.calendar_to.setSelectedDate(self.__to_date)
            return QMessanger().show_message('To date must be greater than from date', 'Warning', QMessageBox.Warning)
        self.__to_date = to_date

    def __import_regions(self):
        self.__weather_api = get_dataframe_from_table(WEATHER_TABLE)
        self.comboBox.addItems(self.__weather_api['region'].unique())
        self.calendar_from.setEnabled(True)
        self.calendar_to.setEnabled(True)
        self.__region = self.comboBox.currentText()
        self.__set_date_range()

    def __choose_region(self):
        self.__region = self.comboBox.currentText()
        self.__set_date_range()

    def __set_date_range(self):
        self.__from_date = min_date = pd.to_datetime(
            self.__weather_api[self.__weather_api['region'] == self.__region]['datetime'] \
                .min())
        self.__to_date = max_date = pd.to_datetime(
            self.__weather_api[self.__weather_api['region'] == self.__region]['datetime'] \
                .max())
        self.calendar_from.setSelectedDate(min_date)
        self.calendar_to.setSelectedDate(max_date)
        self.calendar_from.setDateRange(min_date, max_date)
        self.calendar_to.setDateRange(min_date, max_date)
