from PyQt5 import QtWidgets, QtCore

from app.consts import RED_ROSE


class UiTab1(QtWidgets.QWidget):

    def setupUi(self, MainWindow):
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 30, 1011, 541))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QtWidgets.QTableView(self.horizontalLayoutWidget)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_import_files = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_import_files.setObjectName("button_import_files")
        self.gridLayout_2.addWidget(self.button_import_files, 0, 0, 1, 1)
        self.button_fill_gaps = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_fill_gaps.setObjectName("button_fill_gaps")
        self.gridLayout_2.addWidget(self.button_fill_gaps, 2, 0, 1, 1)
        self.button_export_files = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_export_files.setObjectName("button_export_files")
        self.gridLayout_2.addWidget(self.button_export_files, 4, 0, 1, 1)
        self.button_locate_gaps = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_locate_gaps.setObjectName("button_locate_gaps")
        self.gridLayout_2.addWidget(self.button_locate_gaps, 1, 0, 1, 1)
        self.button_safe_db = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.button_safe_db.setObjectName("button_safe_db")
        self.gridLayout_2.addWidget(self.button_safe_db, 3, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.button_import_files.setText(_translate(RED_ROSE, "Import excel files"))
        self.button_fill_gaps.setText(_translate(RED_ROSE, "Fill gaps"))
        self.button_export_files.setText(_translate(RED_ROSE, "Export excel file"))
        self.button_locate_gaps.setText(_translate(RED_ROSE, "Locate gaps"))
        self.button_safe_db.setText(_translate(RED_ROSE, "Safe to database"))
