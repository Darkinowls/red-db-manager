# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from app.consts import RED_ROSE


class UiMainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(923, 677)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(710, 30, 191, 581))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_locate_gaps = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_locate_gaps.setObjectName("button_locate_gaps")
        self.gridLayout_2.addWidget(self.button_locate_gaps, 1, 0, 1, 1)
        self.button_export_files = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_export_files.setObjectName("button_export_files")
        self.gridLayout_2.addWidget(self.button_export_files, 4, 0, 1, 1)
        self.button_import_files = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_import_files.setObjectName("button_import_files")
        self.gridLayout_2.addWidget(self.button_import_files, 0, 0, 1, 1)
        self.button_fill_gaps = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_fill_gaps.setObjectName("button_fill_gaps")
        self.gridLayout_2.addWidget(self.button_fill_gaps, 2, 0, 1, 1)
        self.button_safe_db = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_safe_db.setObjectName("button_safe_db")
        self.gridLayout_2.addWidget(self.button_safe_db, 3, 0, 1, 1)
        self.button_activate = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_activate.setObjectName("button_activate")
        self.gridLayout_2.addWidget(self.button_activate, 5, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(20, 30, 671, 581))
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 923, 32))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(RED_ROSE, RED_ROSE))
        self.button_safe_db.setText(_translate(RED_ROSE, "Safe to database"))
        self.button_locate_gaps.setText(_translate(RED_ROSE, "Locate gaps"))
        self.button_export_files.setText(_translate(RED_ROSE, "Export excel file"))
        self.button_fill_gaps.setText(_translate(RED_ROSE, "Fill gaps"))
        self.button_activate.setText(_translate(RED_ROSE, "Activate program"))
        self.button_import_files.setText(_translate(RED_ROSE, "Import excel files"))
        # self.button_test_captcha.setText(_translate(RED_ROSE, "Test captcha"))
