# def main():
#     paths = get_files_paths(DIR_NAME)
#     excel_dataframes = read_excel_files(paths)
#     weather_api = get_weather_api(excel_dataframes, paths)
#     weather_marked = locate_datetime_gaps(weather_api)
#     if weather_api is not weather_marked:
#         weather_api = ask_fill_method(weather_marked, [TEMPERATURE, WIND_SPEED], [WIND_DIRECTION_ID])
#     elif weather_api[WIND_DIRECTION_ID].isnull().values.any() and ask_do_use_pad():
#         weather_api = fill_gaps_by_pad(weather_api, [WIND_DIRECTION_ID])
#     renew_database_table(weather_api, WEATHER_TABLE)
#
#
# main()

import sys

from PyQt5 import QtWidgets
from app.windows.MainWindow import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

