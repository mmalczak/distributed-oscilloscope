# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 1071, 651))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 720, 1071, 171))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.inputs_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
        self.inputs_layout.setObjectName("inputs_layout")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(1330, 0, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.horizontal_settings_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.horizontal_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_settings_layout.setObjectName("horizontal_settings_layout")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(1330, 100, 160, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.run_control_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.run_control_layout.setContentsMargins(0, 0, 0, 0)
        self.run_control_layout.setObjectName("run_control_layout")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(1090, 680, 401, 211))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.vertical_settings_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.vertical_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_settings_layout.setObjectName("vertical_settings_layout")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(1090, 440, 160, 201))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.triggers_settings_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.triggers_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.triggers_settings_layout.setObjectName("triggers_settings_layout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

from pyqtgraph import PlotWidget
