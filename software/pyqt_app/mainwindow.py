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
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 1031, 781))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 820, 1031, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.inputs_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
        self.inputs_layout.setObjectName("inputs_layout")
        self.vertical_settings_frame = QtWidgets.QFrame(self.centralwidget)
        self.vertical_settings_frame.setGeometry(QtCore.QRect(1050, 610, 441, 281))
        self.vertical_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.vertical_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.vertical_settings_frame.setObjectName("vertical_settings_frame")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.vertical_settings_frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 60, 401, 211))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.vertical_settings_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.vertical_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_settings_layout.setObjectName("vertical_settings_layout")
        self.vertical_settings_label = QtWidgets.QLabel(self.vertical_settings_frame)
        self.vertical_settings_label.setGeometry(QtCore.QRect(0, 0, 131, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.vertical_settings_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.vertical_settings_label.setFont(font)
        self.vertical_settings_label.setObjectName("vertical_settings_label")
        self.trigger_settings_frame = QtWidgets.QFrame(self.centralwidget)
        self.trigger_settings_frame.setGeometry(QtCore.QRect(1050, 310, 210, 281))
        self.trigger_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trigger_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trigger_settings_frame.setObjectName("trigger_settings_frame")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.trigger_settings_frame)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 60, 160, 201))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.triggers_settings_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.triggers_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.triggers_settings_layout.setObjectName("triggers_settings_layout")
        self.trigger_settings_label = QtWidgets.QLabel(self.trigger_settings_frame)
        self.trigger_settings_label.setGeometry(QtCore.QRect(0, 0, 131, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.trigger_settings_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trigger_settings_label.setFont(font)
        self.trigger_settings_label.setObjectName("trigger_settings_label")
        self.run_control_frame = QtWidgets.QFrame(self.centralwidget)
        self.run_control_frame.setGeometry(QtCore.QRect(1280, 310, 210, 281))
        self.run_control_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.run_control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.run_control_frame.setObjectName("run_control_frame")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.run_control_frame)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 180, 160, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.run_control_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.run_control_layout.setContentsMargins(0, 0, 0, 0)
        self.run_control_layout.setObjectName("run_control_layout")
        self.run_control_label = QtWidgets.QLabel(self.run_control_frame)
        self.run_control_label.setGeometry(QtCore.QRect(0, 0, 111, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.run_control_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.run_control_label.setFont(font)
        self.run_control_label.setObjectName("run_control_label")
        self.horizontal_settings_frame = QtWidgets.QFrame(self.centralwidget)
        self.horizontal_settings_frame.setGeometry(QtCore.QRect(1050, 10, 210, 281))
        self.horizontal_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.horizontal_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontal_settings_frame.setObjectName("horizontal_settings_frame")
        self.horizontal_settings_label = QtWidgets.QLabel(self.horizontal_settings_frame)
        self.horizontal_settings_label.setGeometry(QtCore.QRect(0, 0, 161, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.horizontal_settings_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.horizontal_settings_label.setFont(font)
        self.horizontal_settings_label.setObjectName("horizontal_settings_label")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.horizontal_settings_frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 170, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.horizontal_settings_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.horizontal_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_settings_layout.setObjectName("horizontal_settings_layout")
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
        self.vertical_settings_label.setText(_translate("MainWindow", "Vertical Settings"))
        self.trigger_settings_label.setText(_translate("MainWindow", "Trigger Settings"))
        self.run_control_label.setText(_translate("MainWindow", "Run Control"))
        self.horizontal_settings_label.setText(_translate("MainWindow", "Horizontal Settings"))

from pyqtgraph import PlotWidget
